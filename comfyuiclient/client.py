import io
import sys
import uuid
import json
import time
import random
import requests
import aiohttp
from PIL import Image


def convert_workflow_to_api(workflow_json):
    """
    Convert ComfyUI workflow format to API format.
    
    Args:
        workflow_json: Dict or path to workflow.json file
        
    Returns:
        API format dict ready for ComfyUI API
    """
    # Load from file if path is provided
    if isinstance(workflow_json, str):
        with open(workflow_json, 'r', encoding='utf8') as f:
            workflow_json = json.load(f)
    
    api_json = {}
    
    # Create link lookup table
    link_map = {}
    for link in workflow_json.get('links', []):
        # link format: [link_id, source_node, source_slot, target_node, target_slot, type]
        link_id = link[0]
        source_node = link[1]
        source_slot = link[2]
        link_map[link_id] = [str(source_node), source_slot]
    
    # Widget value mappings for different node types
    widget_mappings = {
        'KSampler': ['seed', 'seed_control', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise'],
        'CLIPTextEncode': ['text'],
        'EmptyLatentImage': ['width', 'height', 'batch_size'],
        'CheckpointLoaderSimple': ['ckpt_name'],
        'SaveImage': ['filename_prefix'],
        'PreviewImage': [],
        'VAEDecode': [],
        'VAEEncode': [],
        'VAELoader': ['vae_name'],
        'LoraLoader': ['lora_name', 'strength_model', 'strength_clip'],
        'ControlNetLoader': ['control_net_name'],
        'LoadImage': ['image', 'upload'],
        'ImageScale': ['upscale_method', 'width', 'height', 'crop'],
    }
    
    # Process each node
    for node in workflow_json.get('nodes', []):
        node_id = str(node['id'])
        node_type = node['type']
        
        api_node = {
            'class_type': node_type,
            '_meta': {
                'title': node.get('title', node_type)
            }
        }
        
        inputs = {}
        
        # Map widget values to named inputs
        widget_values = node.get('widgets_values', [])
        if node_type in widget_mappings:
            param_names = widget_mappings[node_type]
            for i, param_name in enumerate(param_names):
                if i < len(widget_values):
                    # Skip "randomize" value for seed_control in KSampler
                    if param_name == 'seed_control' and widget_values[i] == 'randomize':
                        continue
                    inputs[param_name] = widget_values[i]
        
        # Add connected inputs
        for input_def in node.get('inputs', []):
            if 'link' in input_def and input_def['link'] is not None:
                input_name = input_def['name'].lower().replace(' ', '_')
                inputs[input_name] = link_map.get(input_def['link'])
        
        api_node['inputs'] = inputs
        api_json[node_id] = api_node
    
    return api_json


class ComfyUIClientAsync:

    def __init__(self, server, prompt_file, debug=False):
        self.PROMPT_FILE = prompt_file
        self.SERVER_ADDRESS = server
        self.CLIENT_ID = str(uuid.uuid4())
        self.ws = None
        self.session = None
        self.debug = debug

        self.reload()
    
    def reload(self):
        """Reload workflow file and convert if needed"""
        try:
            with open(self.PROMPT_FILE, 'r', encoding='utf8') as f:
                data = json.load(f)
            
            # Convert workflow.json to API format if needed
            if 'nodes' in data and 'links' in data:
                self.comfyui_prompt = convert_workflow_to_api(data)
            else:
                self.comfyui_prompt = data
                
            if self.debug:
                print(f"Loaded workflow from {self.PROMPT_FILE}")
        except FileNotFoundError:
            print(f"Prompt file not found: {self.PROMPT_FILE}")
        except json.JSONDecodeError:
            print(f"Failed to parse prompt file: {self.PROMPT_FILE}")
        except Exception as e:
            print(f"Error: {e} while reading prompt file: {self.PROMPT_FILE}")

    async def connect(self):
        try:
            self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect(f"ws://{self.SERVER_ADDRESS}/ws?clientId={self.CLIENT_ID}")
        except aiohttp.ClientError as e:
            if self.session:
                await self.session.close()
            raise ConnectionError(f"Failed to connect to ComfyUI server: {e}")

    async def close(self):
        try:
            if self.ws:
                await self.ws.close()
        except Exception as e:
            if self.debug:
                print(f"Error closing WebSocket: {e}")
        try:
            if self.session:
                await self.session.close()
        except Exception as e:
            if self.debug:
                print(f"Error closing session: {e}")

    async def queue_prompt(self, prompt):
        try:
            payload = {"prompt": prompt, "client_id": self.CLIENT_ID}
            async with self.session.post(f"http://{self.SERVER_ADDRESS}/prompt", json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                if 'prompt_id' not in result:
                    raise ValueError("Server response missing prompt_id")
                return result
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to queue prompt: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from server: {e}")

    async def get_image(self, filename, subfolder, folder_type):
        try:
            params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
            async with self.session.get(f"http://{self.SERVER_ADDRESS}/view", params=params) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to get image {filename}: {e}")

    async def get_history(self, prompt_id):
        try:
            async with self.session.get(f"http://{self.SERVER_ADDRESS}/history/{prompt_id}") as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to get history for {prompt_id}: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from server: {e}")

    async def get_images(self, prompt):
        prompt_id = (await self.queue_prompt(prompt))['prompt_id']
        output_images = {}
        output_text = {}

        while True:
            message = await self.ws.receive()
            if message.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(message.data)
                if data['type'] == 'executing' and data['data']['node'] is None and data['data']['prompt_id'] == prompt_id:
                    break
        
        history = (await self.get_history(prompt_id))[prompt_id]
        for node_id, node_output in history['outputs'].items():
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = await self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
            if 'text' in node_output:
                output_text[node_id] = node_output['text']
        
        return output_images, output_text
    
    async def set_data(self, key, text:str=None, seed:int=None, image:Image.Image=None, 
                       number:float=None, value:float=None, input_key:str=None, input_value=None):
        key_id = self.find_key_by_title(key)
        if key_id is None:
            return
            
        if input_key is not None and input_value is not None:
            self.comfyui_prompt[key_id]['inputs'][input_key] = input_value
        if text is not None:
            self.comfyui_prompt[key_id]['inputs']['text'] = text
        if seed is not None:
            self.comfyui_prompt[key_id]['inputs']['seed'] = int(seed)
        if number is not None:
            self.comfyui_prompt[key_id]['inputs']['Number'] = number
        if value is not None:
            self.comfyui_prompt[key_id]['inputs']['value'] = value
        if image is not None:
            try:
                # Upload image to comfyui server
                folder_name = "temp"
                
                # Save image to byte data
                byte_data = io.BytesIO()
                image.save(byte_data, format="PNG")
                byte_data.seek(0)

                # Upload image using existing session
                data = aiohttp.FormData()
                data.add_field('image', byte_data, filename="temp.png")
                data.add_field('subfolder', folder_name)
                
                async with self.session.post(
                    f"http://{self.SERVER_ADDRESS}/upload/image",
                    data=data
                ) as response:
                    response.raise_for_status()
                    resp_json = await response.json()
                    
                    if 'name' not in resp_json or 'subfolder' not in resp_json:
                        raise ValueError("Invalid upload response: missing required fields")
                
                # Set image path
                self.comfyui_prompt[key_id]['inputs']['image'] = resp_json.get('subfolder') + '/' + resp_json.get('name')
            except aiohttp.ClientError as e:
                raise ConnectionError(f"Failed to upload image: {e}")
            except Exception as e:
                raise RuntimeError(f"Error processing image upload: {e}")
        
        if self.debug:
            print(f"Set data for {key} (id: {key_id}): {self.comfyui_prompt[key_id]}")

    def find_key_by_title(self, target_title):
        target_title = target_title.strip()
        for key, value in self.comfyui_prompt.items():
            # Check class_type first
            class_type = value.get('class_type', '').strip()
            if class_type == target_title:
                return key
            # Then check title
            title = value.get('_meta', {}).get('title', '').strip()
            if title == target_title:
                return key
        if self.debug:
            print(f"Key not found: {target_title}")
        return None

    async def generate(self, node_names=None) -> dict:
        node_ids = {}
        if node_names is not None:
            for node_name in node_names:
                node_id = self.find_key_by_title(node_name)
                if node_id is not None:
                    node_ids[node_id] = node_name

        images, text = await self.get_images(self.comfyui_prompt)
        results = {}
        for node_id, node_images in images.items():
            if node_id in node_ids:
                for image_data in node_images:
                    image = Image.open(io.BytesIO(image_data))
                    results[node_ids[node_id]] = image
        for node_id, node_text in text.items():
            if node_id in node_ids:
                results[node_ids[node_id]] = node_text

        return results


class ComfyUIClient:

    def __init__(self, server, prompt_file, debug=False):
        self.PROMPT_FILE = prompt_file
        self.SERVER_ADDRESS = server
        self.CLIENT_ID = str(uuid.uuid4())
        self.session = None
        self.debug = debug

        self.reload()
    
    def reload(self):
        """Reload workflow file and convert if needed"""
        try:
            with open(self.PROMPT_FILE, 'r', encoding='utf8') as f:
                data = json.load(f)
            
            # Convert workflow.json to API format if needed
            if 'nodes' in data and 'links' in data:
                self.comfyui_prompt = convert_workflow_to_api(data)
            else:
                self.comfyui_prompt = data
                
            if self.debug:
                print(f"Loaded workflow from {self.PROMPT_FILE}")
        except FileNotFoundError:
            print(f"Prompt file not found: {self.PROMPT_FILE}")
        except json.JSONDecodeError:
            print(f"Failed to parse prompt file: {self.PROMPT_FILE}")
        except Exception as e:
            print(f"Error: {e} while reading prompt file: {self.PROMPT_FILE}")

    def connect(self):
        self.session = requests.Session()

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None

    def queue_prompt(self, prompt):
        try:
            payload = {"prompt": prompt, "client_id": self.CLIENT_ID}
            response = self.session.post(
                f"http://{self.SERVER_ADDRESS}/prompt", 
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            if 'prompt_id' not in result:
                raise ValueError("Server response missing prompt_id")
            return result
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to queue prompt: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from server: {e}")

    def get_image(self, filename, subfolder, folder_type):
        try:
            params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
            response = self.session.get(f"http://{self.SERVER_ADDRESS}/view", params=params)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to get image {filename}: {e}")

    def get_history(self, prompt_id):
        try:
            response = self.session.get(f"http://{self.SERVER_ADDRESS}/history/{prompt_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to get history for {prompt_id}: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from server: {e}")

    def get_images(self, prompt):
        result = self.queue_prompt(prompt)
        prompt_id = result.get('prompt_id')
        if not prompt_id:
            raise ValueError("Failed to get prompt_id from server response")
            
        output_images = {}
        output_text = {}
        max_retries = 300  # Maximum 5 minutes wait
        retry_count = 0

        while retry_count < max_retries:
            try:
                history = self.get_history(prompt_id)
                if prompt_id in history and 'outputs' in history[prompt_id]:
                    break
                time.sleep(1)
                retry_count += 1
            except Exception as e:
                if self.debug:
                    print(f"Error getting history (retry {retry_count}): {e}")
                if retry_count >= max_retries:
                    raise TimeoutError(f"Timeout waiting for prompt {prompt_id} to complete")
                time.sleep(1)
                retry_count += 1
        
        if retry_count >= max_retries:
            raise TimeoutError(f"Timeout waiting for prompt {prompt_id} to complete")
        
        for node_id, node_output in history[prompt_id]['outputs'].items():
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
            if 'text' in node_output:
                output_text[node_id] = node_output['text']
        
        return output_images, output_text
    
    def set_data(self, key, text:str=None, seed:int=None, image:Image.Image=None, 
                 number:float=None, value:float=None, input_key:str=None, input_value=None):
        key_id = self.find_key_by_title(key)
        if key_id is None:
            return
            
        if input_key is not None and input_value is not None:
            self.comfyui_prompt[key_id]['inputs'][input_key] = input_value
        if text is not None:
            self.comfyui_prompt[key_id]['inputs']['text'] = text
        if seed is not None:
            self.comfyui_prompt[key_id]['inputs']['seed'] = int(seed)
        if number is not None:
            self.comfyui_prompt[key_id]['inputs']['Number'] = number
        if value is not None:
            self.comfyui_prompt[key_id]['inputs']['value'] = value
        if image is not None:
            # Upload image to comfyui server
            folder_name = "temp"
            
            # Save image to byte data
            byte_data = io.BytesIO()
            image.save(byte_data, format="PNG")
            byte_data.seek(0)

            # Upload image
            try:
                resp = self.session.post(
                    f"http://{self.SERVER_ADDRESS}/upload/image", 
                    files={'image': ("temp.png", byte_data)}, 
                    data={"subfolder": folder_name})
                resp.raise_for_status()
                
                resp_json = resp.json()
                if 'name' not in resp_json or 'subfolder' not in resp_json:
                    raise ValueError("Invalid upload response: missing required fields")
                
                # Set image path
                self.comfyui_prompt[key_id]['inputs']['image'] = resp_json.get('subfolder') + '/' + resp_json.get('name')
            except requests.RequestException as e:
                raise ConnectionError(f"Failed to upload image: {e}")
            except Exception as e:
                raise RuntimeError(f"Error processing image upload: {e}")
        
        if self.debug:
            print(f"Set data for {key} (id: {key_id}): {self.comfyui_prompt[key_id]}")

    def find_key_by_title(self, target_title):
        target_title = target_title.strip()
        for key, value in self.comfyui_prompt.items():
            # Check class_type first
            class_type = value.get('class_type', '').strip()
            if class_type == target_title:
                return key
            # Then check title
            title = value.get('_meta', {}).get('title', '').strip()
            if title == target_title:
                return key
        if self.debug:
            print(f"Key not found: {target_title}")
        return None

    def generate(self, node_names=None) -> dict:
        node_ids = {}
        if node_names is not None:
            for node_name in node_names:
                node_id = self.find_key_by_title(node_name)
                if node_id is not None:
                    node_ids[node_id] = node_name

        images, text = self.get_images(self.comfyui_prompt)
        results = {}
        for node_id, node_images in images.items():
            if node_id in node_ids:
                for image_data in node_images:
                    image = Image.open(io.BytesIO(image_data))
                    results[node_ids[node_id]] = image
        for node_id, node_text in text.items():
            if node_id in node_ids:
                results[node_ids[node_id]] = node_text

        return results


def main():
    comfyui_client = None
    try:
        comfyui_client = ComfyUIClient("192.168.1.27:8188", "workflow_api.json", debug=True)
        comfyui_client.connect()
        comfyui_client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        comfyui_client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape painting")
        for key, image in comfyui_client.generate(["Result Image"]).items():
            image.save(f"{key}.png")
            if comfyui_client.debug:
                print(f"Saved {key}.png")
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if comfyui_client is not None:
            comfyui_client.close()


async def main_async():
    comfyui_client = None
    try:
        comfyui_client = ComfyUIClientAsync("192.168.1.27:8188", "workflow_api.json", debug=True)
        await comfyui_client.connect()
        await comfyui_client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        await comfyui_client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape painting")
        for key, image in (await comfyui_client.generate(["Result Image"])).items():
            image.save(f"{key}_async.png")
            if comfyui_client.debug:
                print(f"Saved {key}_async.png")
    except Exception as e:
        print(f"Error in main_async: {e}")
    finally:
        if comfyui_client is not None:
            await comfyui_client.close()


if __name__ == "__main__":
    # non-async
    main()

    # async
    import asyncio
    asyncio.run(main_async())
