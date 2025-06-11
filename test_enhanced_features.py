#!/usr/bin/env python3
"""Test enhanced features from other repositories"""

import random
import sys
from comfyuiclient import ComfyUIClient

def test_enhanced_features():
    """Test the new enhanced features"""
    print("=== Testing Enhanced ComfyUI Client Features ===\n")
    
    # Test with debug mode
    print("1. Testing with debug mode enabled:")
    client = ComfyUIClient("192.168.1.27:8188", "workflow.json", debug=True)
    client.connect()
    
    # Test enhanced set_data with arbitrary input
    print("\n2. Testing enhanced set_data with arbitrary input:")
    client.set_data(key='KSampler', input_key='steps', input_value=15)
    
    # Test number and value parameters
    print("\n3. Testing number and value parameters:")
    client.set_data(key='EmptyLatentImage', number=256.0)
    
    # Test reload functionality
    print("\n4. Testing reload functionality:")
    client.reload()
    
    # Test class_type lookup
    print("\n5. Testing class_type lookup:")
    ksampler_id = client.find_key_by_title('KSampler')
    print(f"Found KSampler by class_type: {ksampler_id}")
    
    # Generate image with enhanced features
    print("\n6. Generating image with enhanced features:")
    client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
    client.set_data(key='CLIP Text Encode Positive', text="enhanced magical forest with glowing mushrooms")
    
    try:
        results = client.generate(["Result Image"])
        for key, image in results.items():
            filename = f"enhanced_test_{key}.png"
            image.save(filename)
            print(f"✓ Success! Saved: {filename}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        client.close()
    
    print("\n✓ Enhanced features test completed!")

if __name__ == "__main__":
    test_enhanced_features()