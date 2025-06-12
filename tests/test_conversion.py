#!/usr/bin/env python3
"""Test conversion from workflow.json to API format"""

import json
from comfyuiclient import convert_workflow_to_api

# Test conversion
print("Testing workflow.json to API format conversion...")

# Convert workflow.json
api_format = convert_workflow_to_api('workflow.json')

# Save converted format
with open('workflow_converted.json', 'w', encoding='utf8') as f:
    json.dump(api_format, f, indent=2, ensure_ascii=False)

print("Converted workflow saved to workflow_converted.json")

# Compare with original workflow_api.json
with open('workflow_api.json', 'r', encoding='utf8') as f:
    original_api = json.load(f)

print("\nComparison with original workflow_api.json:")
print(f"Original nodes: {list(original_api.keys())}")
print(f"Converted nodes: {list(api_format.keys())}")

# Check each node
for node_id in original_api:
    if node_id in api_format:
        print(f"\nNode {node_id} ({original_api[node_id]['class_type']}):")
        orig_inputs = original_api[node_id]['inputs']
        conv_inputs = api_format[node_id]['inputs']
        
        # Compare inputs
        for key in orig_inputs:
            if key in conv_inputs:
                if orig_inputs[key] == conv_inputs[key]:
                    print(f"  ✓ {key}: {orig_inputs[key]}")
                else:
                    print(f"  ✗ {key}: {orig_inputs[key]} → {conv_inputs[key]}")
            else:
                print(f"  - {key}: missing in converted")
        
        # Check for extra inputs in converted
        for key in conv_inputs:
            if key not in orig_inputs:
                print(f"  + {key}: {conv_inputs[key]} (extra in converted)")

print("\nConversion test complete!")