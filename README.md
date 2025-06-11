# ComfyUI API Client

A Python client library for interacting with ComfyUI via its API. Supports both synchronous and asynchronous operations with automatic workflow format conversion.

## Features

- 🔄 **Dual Client Support**: Both sync (`ComfyUIClient`) and async (`ComfyUIClientAsync`) implementations
- 🎯 **Automatic Format Detection**: Automatically converts `workflow.json` to API format
- 🛠️ **Enhanced Configuration**: Flexible `set_data()` method for all parameter types
- 🐛 **Debug Mode**: Optional debug output for development and troubleshooting
- 🔧 **Dynamic Reload**: Reload workflow files without restarting
- 🛡️ **Robust Error Handling**: Comprehensive error handling with user-friendly messages
- 🔍 **Smart Node Lookup**: Find nodes by title or class_type
- 📦 **Image Upload Support**: Direct image upload to ComfyUI server

## Installation

```bash
pip install -r requirements.txt
```

### Requirements

```
requests
aiohttp
Pillow
```

## Quick Start

### Synchronous Client

```python
from comfyuiclient import ComfyUIClient

# Initialize client (supports both workflow.json and workflow_api.json)
client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

# Set parameters
client.set_data(key='KSampler', seed=12345)
client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape")

# Generate images
results = client.generate(["Result Image"])
for key, image in results.items():
    image.save(f"{key}.png")

client.close()
```

### Asynchronous Client

```python
import asyncio
from comfyuiclient import ComfyUIClientAsync

async def main():
    # Initialize async client
    client = ComfyUIClientAsync("localhost:8188", "workflow.json")
    await client.connect()
    
    # Set parameters (all async)
    await client.set_data(key='KSampler', seed=12345)
    await client.set_data(key='CLIP Text Encode Positive', text="beautiful landscape")
    
    # Generate images
    results = await client.generate(["Result Image"])
    for key, image in results.items():
        image.save(f"{key}.png")
    
    await client.close()

asyncio.run(main())
```

## API Reference

### Client Initialization

```python
# Basic initialization
client = ComfyUIClient(server_address, workflow_file)

# With debug mode
client = ComfyUIClient(server_address, workflow_file, debug=True)
```

**Parameters:**
- `server_address`: ComfyUI server address (e.g., "localhost:8188")
- `workflow_file`: Path to workflow.json or workflow_api.json
- `debug`: Enable debug output (default: False)

### Core Methods

#### `connect()`
Establishes connection to ComfyUI server.

```python
# Sync
client.connect()

# Async
await client.connect()
```

#### `set_data(key, **kwargs)`
Sets parameters for workflow nodes.

```python
# Basic parameters
client.set_data(key='KSampler', seed=12345)
client.set_data(key='CLIP Text Encode Positive', text="prompt text")

# Advanced parameters
client.set_data(key='KSampler', input_key='steps', input_value=25)
client.set_data(key='EmptyLatentImage', number=512.0)
client.set_data(key='SomeNode', value=1.5)

# Image upload
from PIL import Image
image = Image.open("input.png")
client.set_data(key='LoadImage', image=image)
```

**Parameters:**
- `key`: Node title or class_type
- `text`: Text input for text nodes
- `seed`: Seed value for generation nodes
- `image`: PIL Image object for image inputs
- `number`: Numeric parameter (mapped to 'Number' input)
- `value`: Numeric parameter (mapped to 'value' input)
- `input_key`/`input_value`: Arbitrary key-value pairs

#### `generate(node_names=None)`
Generates outputs from specified nodes.

```python
# Generate from specific nodes
results = client.generate(["Result Image", "Preview"])

# Generate from all output nodes
results = client.generate()

# Results are returned as {node_name: PIL.Image} dictionary
for node_name, image in results.items():
    image.save(f"{node_name}.png")
```

#### `reload()`
Reloads the workflow file (useful for dynamic workflows).

```python
client.reload()
```

#### `close()`
Closes the connection and cleans up resources.

```python
# Sync
client.close()

# Async
await client.close()
```

### Utility Functions

#### `convert_workflow_to_api(workflow_json)`
Converts ComfyUI workflow format to API format.

```python
from comfyuiclient import convert_workflow_to_api

# Convert file
api_format = convert_workflow_to_api("workflow.json")

# Convert dict
with open("workflow.json") as f:
    workflow_data = json.load(f)
api_format = convert_workflow_to_api(workflow_data)
```

## Workflow File Support

The client automatically detects and handles both workflow formats:

### workflow.json (ComfyUI Editor Format)
- Exported from ComfyUI web interface
- Contains UI layout and visual information
- **Automatically converted** to API format

### workflow_api.json (ComfyUI API Format)
- API-ready format
- **Used directly** without conversion

Example of automatic detection:
```python
# Both work seamlessly
client1 = ComfyUIClient("localhost:8188", "workflow.json")      # Auto-converted
client2 = ComfyUIClient("localhost:8188", "workflow_api.json")  # Direct use
```

## Error Handling

The client provides comprehensive error handling:

```python
try:
    client = ComfyUIClient("localhost:8188", "workflow.json")
    client.connect()
    results = client.generate(["Result Image"])
except ConnectionError as e:
    print(f"Connection failed: {e}")
except ValueError as e:
    print(f"Invalid data: {e}")
except TimeoutError as e:
    print(f"Operation timed out: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    client.close()
```

## Debug Mode

Enable debug mode for detailed logging:

```python
client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
```

Debug output includes:
- Workflow loading status
- Parameter setting details
- Node lookup information
- Error details and retry attempts

## Advanced Examples

### Context Manager Pattern

```python
class ComfyUIContextManager:
    def __init__(self, *args, **kwargs):
        self.client = ComfyUIClient(*args, **kwargs)
    
    def __enter__(self):
        self.client.connect()
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

# Usage
with ComfyUIContextManager("localhost:8188", "workflow.json") as client:
    client.set_data(key='KSampler', seed=12345)
    results = client.generate(["Result Image"])
```

### Batch Processing

```python
import random

prompts = ["sunset over mountains", "city at night", "forest lake"]
seeds = [random.randint(0, 2**32) for _ in range(3)]

client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

for i, (prompt, seed) in enumerate(zip(prompts, seeds)):
    client.set_data(key='CLIP Text Encode Positive', text=prompt)
    client.set_data(key='KSampler', seed=seed)
    
    results = client.generate(["Result Image"])
    for key, image in results.items():
        image.save(f"output_{i}_{key}.png")

client.close()
```

### Dynamic Workflow Updates

```python
client = ComfyUIClient("localhost:8188", "workflow.json")
client.connect()

# Initial generation
client.set_data(key='KSampler', seed=12345)
results = client.generate(["Result Image"])

# Modify workflow file externally, then reload
client.reload()

# Use updated workflow
client.set_data(key='KSampler', seed=67890)
results = client.generate(["Result Image"])

client.close()
```

## Testing

Run the test suite:

```bash
# Basic functionality tests
python test_workflow_loading.py

# Error handling tests
python test_error_handling.py

# Enhanced features tests
python test_enhanced_features.py

# Format conversion tests
python test_conversion.py
```

## Troubleshooting

### Common Issues

**1. Connection Refused**
```
ConnectionError: Failed to connect to ComfyUI server
```
- Ensure ComfyUI is running on the specified address
- Check firewall settings
- Verify the port number

**2. Key Not Found**
```
Key not found: NodeName
```
- Check node title in ComfyUI interface
- Try using class_type instead of title
- Enable debug mode to see available nodes

**3. Timeout Errors**
```
TimeoutError: Timeout waiting for prompt to complete
```
- Complex workflows may take longer than 5 minutes
- Check ComfyUI server performance
- Verify workflow is valid

### Debug Tips

1. **Enable debug mode** for detailed logs:
   ```python
   client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
   ```

2. **Check node names** in your workflow:
   ```python
   client = ComfyUIClient("localhost:8188", "workflow.json", debug=True)
   # Debug output will show available node IDs and titles
   ```

3. **Test workflow in ComfyUI first** before using the client

4. **Use format conversion** to understand your workflow:
   ```python
   api_format = convert_workflow_to_api("workflow.json")
   print(json.dumps(api_format, indent=2))
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Changelog

### Latest Version
- ✅ Enhanced error handling with specific exception types
- ✅ Debug mode for development and troubleshooting  
- ✅ Automatic workflow.json to API format conversion
- ✅ Dynamic workflow reloading
- ✅ Enhanced set_data() with arbitrary parameter support
- ✅ Smart node lookup by title or class_type
- ✅ Comprehensive test suite
- ✅ Timeout handling for long-running operations
- ✅ Robust resource cleanup
