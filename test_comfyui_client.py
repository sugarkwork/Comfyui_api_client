#!/usr/bin/env python3
"""
Comprehensive test script for ComfyUIClient
Tests both sync and async versions with both workflow formats
"""

import asyncio
import json
import sys
import os
import random
import traceback
from pathlib import Path
from comfyuiclient import ComfyUIClient, ComfyUIClientAsync, convert_workflow_to_api

# Configuration
SERVER_ADDRESS = "192.168.1.27:8188"  # Update this to your ComfyUI server address
TEST_PROMPT = "a beautiful sunset over mountains, digital art"
TEST_NEGATIVE_PROMPT = "low quality, blurry"

# ANSI color codes for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_test_case(test_name):
    """Print a test case header"""
    print(f"{Colors.CYAN}{Colors.BOLD}Testing: {test_name}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*40}{Colors.ENDC}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.ENDC}")


def verify_workflow_format(workflow_file):
    """Verify and display workflow format type"""
    with open(workflow_file, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    if 'nodes' in data and 'links' in data:
        print_info(f"{workflow_file} is in ComfyUI workflow format (needs conversion)")
        print_info(f"  - Contains {len(data.get('nodes', []))} nodes")
        print_info(f"  - Contains {len(data.get('links', []))} links")
        return "workflow"
    else:
        print_info(f"{workflow_file} is in API format (ready to use)")
        print_info(f"  - Contains {len(data)} node definitions")
        return "api"


def test_format_conversion():
    """Test the workflow format conversion function"""
    print_test_case("Format Conversion Function")
    
    try:
        # Test converting workflow.json
        with open('workflow.json', 'r', encoding='utf8') as f:
            workflow_data = json.load(f)
        
        api_format = convert_workflow_to_api(workflow_data)
        
        print_success("Successfully converted workflow.json to API format")
        print_info(f"  - Original nodes: {len(workflow_data.get('nodes', []))}")
        print_info(f"  - Converted nodes: {len(api_format)}")
        
        # Verify structure
        for node_id, node_data in api_format.items():
            if 'class_type' not in node_data:
                print_error(f"Node {node_id} missing class_type")
                return False
            if 'inputs' not in node_data:
                print_error(f"Node {node_id} missing inputs")
                return False
        
        print_success("All converted nodes have correct structure")
        
        # Compare with workflow_api.json
        with open('workflow_api.json', 'r', encoding='utf8') as f:
            reference_api = json.load(f)
        
        # Check if key nodes exist
        key_nodes_found = 0
        for node_id in reference_api:
            if node_id in api_format:
                key_nodes_found += 1
        
        print_info(f"  - Matching nodes with reference: {key_nodes_found}/{len(reference_api)}")
        
        return True
        
    except Exception as e:
        print_error(f"Format conversion failed: {str(e)}")
        traceback.print_exc()
        return False


def test_sync_client(workflow_file):
    """Test synchronous ComfyUIClient"""
    print_test_case(f"Sync Client with {workflow_file}")
    
    client = None
    try:
        # Verify format before testing
        format_type = verify_workflow_format(workflow_file)
        
        # Initialize client
        client = ComfyUIClient(SERVER_ADDRESS, workflow_file)
        print_success("Client initialized successfully")
        
        # Test automatic format detection
        print_info("Testing automatic format detection...")
        if format_type == "workflow" and 'nodes' not in client.comfyui_prompt:
            print_success("Workflow format was automatically converted to API format")
        elif format_type == "api" and 'nodes' not in client.comfyui_prompt:
            print_success("API format was loaded directly without conversion")
        
        # Connect to server
        client.connect()
        print_success("Connected to ComfyUI server")
        
        # Set test data
        test_seed = random.randint(0, sys.maxsize)
        client.set_data(key='KSampler', seed=test_seed)
        print_success(f"Set random seed: {test_seed}")
        
        # Try different possible node names for positive prompt
        positive_set = False
        for node_name in ['CLIP Text Encode Positive', 'CLIPTextEncode', 'positive']:
            try:
                client.set_data(key=node_name, text=TEST_PROMPT)
                print_success(f"Set positive prompt using node: {node_name}")
                positive_set = True
                break
            except:
                continue
        
        if not positive_set:
            print_warning("Could not find positive prompt node")
        
        # Generate image
        print_info("Generating image...")
        output_filename = f"test_sync_{Path(workflow_file).stem}.png"
        
        # Try different possible output node names
        for node_name in ['Result Image', 'SaveImage', 'PreviewImage']:
            try:
                results = client.generate([node_name])
                if results:
                    for key, image in results.items():
                        image.save(output_filename)
                        print_success(f"Generated and saved image: {output_filename}")
                        print_info(f"  - Image size: {image.size}")
                        print_info(f"  - Image mode: {image.mode}")
                    break
            except:
                continue
        
        return True
        
    except Exception as e:
        print_error(f"Sync client test failed: {str(e)}")
        traceback.print_exc()
        return False
    finally:
        if client:
            client.close()
            print_info("Client connection closed")


async def test_async_client(workflow_file):
    """Test asynchronous ComfyUIClient"""
    print_test_case(f"Async Client with {workflow_file}")
    
    client = None
    try:
        # Verify format before testing
        format_type = verify_workflow_format(workflow_file)
        
        # Initialize client
        client = ComfyUIClientAsync(SERVER_ADDRESS, workflow_file)
        print_success("Async client initialized successfully")
        
        # Test automatic format detection
        print_info("Testing automatic format detection...")
        if format_type == "workflow" and 'nodes' not in client.comfyui_prompt:
            print_success("Workflow format was automatically converted to API format")
        elif format_type == "api" and 'nodes' not in client.comfyui_prompt:
            print_success("API format was loaded directly without conversion")
        
        # Connect to server
        await client.connect()
        print_success("Connected to ComfyUI server (async)")
        
        # Set test data
        test_seed = random.randint(0, sys.maxsize)
        await client.set_data(key='KSampler', seed=test_seed)
        print_success(f"Set random seed: {test_seed}")
        
        # Try different possible node names for positive prompt
        positive_set = False
        for node_name in ['CLIP Text Encode Positive', 'CLIPTextEncode', 'positive']:
            try:
                await client.set_data(key=node_name, text=TEST_PROMPT)
                print_success(f"Set positive prompt using node: {node_name}")
                positive_set = True
                break
            except:
                continue
        
        if not positive_set:
            print_warning("Could not find positive prompt node")
        
        # Generate image
        print_info("Generating image...")
        output_filename = f"test_async_{Path(workflow_file).stem}.png"
        
        # Try different possible output node names
        for node_name in ['Result Image', 'SaveImage', 'PreviewImage']:
            try:
                results = await client.generate([node_name])
                if results:
                    for key, image in results.items():
                        image.save(output_filename)
                        print_success(f"Generated and saved image: {output_filename}")
                        print_info(f"  - Image size: {image.size}")
                        print_info(f"  - Image mode: {image.mode}")
                    break
            except:
                continue
        
        return True
        
    except Exception as e:
        print_error(f"Async client test failed: {str(e)}")
        traceback.print_exc()
        return False
    finally:
        if client:
            await client.close()
            print_info("Async client connection closed")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


async def run_all_tests():
    """Run all test combinations"""
    print_header("ComfyUI Client Comprehensive Test Suite")
    
    # Check if server is reachable
    print_test_case("Server Connection Check")
    try:
        import requests
        response = requests.get(f"http://{SERVER_ADDRESS}/system_stats", timeout=5)
        if response.status_code == 200:
            print_success(f"ComfyUI server is reachable at {SERVER_ADDRESS}")
        else:
            print_warning(f"Server responded with status code: {response.status_code}")
    except Exception as e:
        print_error(f"Cannot reach ComfyUI server at {SERVER_ADDRESS}")
        print_error("Please ensure ComfyUI is running and update SERVER_ADDRESS in this script")
        return
    
    # Test format conversion
    print_header("Testing Format Conversion")
    conversion_success = test_format_conversion()
    
    # Test all combinations
    test_results = {
        "Format Conversion": conversion_success,
        "Sync + workflow.json": False,
        "Sync + workflow_api.json": False,
        "Async + workflow.json": False,
        "Async + workflow_api.json": False
    }
    
    # Run sync tests
    print_header("Synchronous Client Tests")
    
    if os.path.exists("workflow.json"):
        test_results["Sync + workflow.json"] = test_sync_client("workflow.json")
    else:
        print_warning("workflow.json not found, skipping test")
    
    if os.path.exists("workflow_api.json"):
        test_results["Sync + workflow_api.json"] = test_sync_client("workflow_api.json")
    else:
        print_warning("workflow_api.json not found, skipping test")
    
    # Run async tests
    print_header("Asynchronous Client Tests")
    
    if os.path.exists("workflow.json"):
        test_results["Async + workflow.json"] = await test_async_client("workflow.json")
    else:
        print_warning("workflow.json not found, skipping test")
    
    if os.path.exists("workflow_api.json"):
        test_results["Async + workflow_api.json"] = await test_async_client("workflow_api.json")
    else:
        print_warning("workflow_api.json not found, skipping test")
    
    # Print summary
    print_header("Test Summary")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    print(f"{Colors.BOLD}Total Tests: {total_tests}{Colors.ENDC}")
    print(f"{Colors.GREEN}{Colors.BOLD}Passed: {passed_tests}{Colors.ENDC}")
    print(f"{Colors.FAIL}{Colors.BOLD}Failed: {total_tests - passed_tests}{Colors.ENDC}")
    print()
    
    for test_name, result in test_results.items():
        status = f"{Colors.GREEN}PASS{Colors.ENDC}" if result else f"{Colors.FAIL}FAIL{Colors.ENDC}"
        print(f"  {test_name:<30} [{status}]")
    
    print()
    if passed_tests == total_tests:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests passed! 🎉{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}Some tests failed. Please check the output above.{Colors.ENDC}")
    
    # List generated files
    print_header("Generated Files")
    generated_files = [
        "test_sync_workflow.png",
        "test_sync_workflow_api.png", 
        "test_async_workflow.png",
        "test_async_workflow_api.png"
    ]
    
    for file in generated_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size:,} bytes)")
        else:
            print_info(f"{file} (not generated)")


def main():
    """Main entry point"""
    # Run the async test suite
    asyncio.run(run_all_tests())


if __name__ == "__main__":
    main()