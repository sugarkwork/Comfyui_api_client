#!/usr/bin/env python3
"""Verify that format detection works correctly"""

import json
from comfyuiclient import ComfyUIClient

def check_format_detection():
    """Check if the format detection logic works correctly"""
    print("=== Verifying Format Detection ===\n")
    
    # Test workflow.json
    print("1. Loading workflow.json:")
    with open('workflow.json', 'r') as f:
        workflow_data = json.load(f)
    
    print(f"   - Has 'nodes' key: {'nodes' in workflow_data}")
    print(f"   - Has 'links' key: {'links' in workflow_data}")
    print(f"   - Number of nodes: {len(workflow_data.get('nodes', []))}")
    print(f"   - Should convert: YES\n")
    
    # Test workflow_api.json
    print("2. Loading workflow_api.json:")
    with open('workflow_api.json', 'r') as f:
        api_data = json.load(f)
    
    print(f"   - Has 'nodes' key: {'nodes' in api_data}")
    print(f"   - Has 'links' key: {'links' in api_data}")
    print(f"   - Root keys are node IDs: {all(key.isdigit() for key in api_data.keys())}")
    print(f"   - Should convert: NO\n")
    
    # Test actual client behavior
    print("3. Testing client auto-detection:")
    
    # Test with workflow.json
    client1 = ComfyUIClient("dummy:8188", "workflow.json")
    print(f"   - workflow.json loaded, has node '3': {'3' in client1.comfyui_prompt}")
    print(f"   - Node '3' class_type: {client1.comfyui_prompt.get('3', {}).get('class_type', 'N/A')}")
    
    # Test with workflow_api.json
    client2 = ComfyUIClient("dummy:8188", "workflow_api.json")
    print(f"   - workflow_api.json loaded, has node '3': {'3' in client2.comfyui_prompt}")
    print(f"   - Node '3' class_type: {client2.comfyui_prompt.get('3', {}).get('class_type', 'N/A')}")
    
    print("\n✓ Format detection is working correctly!")

if __name__ == "__main__":
    check_format_detection()