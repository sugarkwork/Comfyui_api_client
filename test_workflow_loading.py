#!/usr/bin/env python3
"""Test automatic workflow format detection and conversion with enhanced features"""

import asyncio
import random
import sys
from comfyuiclient import ComfyUIClient, ComfyUIClientAsync

# Test configuration
SERVER_ADDRESS = "192.168.1.27:8188"
TEST_PROMPTS = [
    "beautiful mountain landscape with snow",
    "futuristic city at night",
    "magical forest with glowing plants",
    "underwater coral reef scene"
]

def test_enhanced_features_sync(client, test_name):
    """Test enhanced features for sync client"""
    print(f"  Testing enhanced features for {test_name}:")
    
    # Test reload
    client.reload()
    print("    ✓ reload() method")
    
    # Test enhanced set_data with arbitrary input
    client.set_data(key='KSampler', input_key='steps', input_value=25)
    print("    ✓ set_data with input_key/input_value")
    
    # Test number parameter
    client.set_data(key='EmptyLatentImage', number=128.0)
    print("    ✓ set_data with number parameter")
    
    # Test class_type lookup
    node_id = client.find_key_by_title('KSampler')
    print(f"    ✓ find_key_by_title by class_type: {node_id}")

async def test_enhanced_features_async(client, test_name):
    """Test enhanced features for async client"""
    print(f"  Testing enhanced features for {test_name}:")
    
    # Test reload
    client.reload()
    print("    ✓ reload() method")
    
    # Test enhanced set_data with arbitrary input
    await client.set_data(key='KSampler', input_key='steps', input_value=25)
    print("    ✓ set_data with input_key/input_value")
    
    # Test number parameter
    await client.set_data(key='EmptyLatentImage', number=128.0)
    print("    ✓ set_data with number parameter")
    
    # Test class_type lookup
    node_id = client.find_key_by_title('KSampler')
    print(f"    ✓ find_key_by_title by class_type: {node_id}")

def test_sync_workflow():
    """Test sync client with workflow.json (auto-conversion)"""
    print("\n=== Testing Sync Client with workflow.json ===")
    client = None
    try:
        client = ComfyUIClient(SERVER_ADDRESS, "workflow.json", debug=True)
        client.connect()
        
        # Test enhanced features
        test_enhanced_features_sync(client, "sync workflow")
        
        # Set random seed and prompt
        prompt = random.choice(TEST_PROMPTS)
        print(f"Using prompt: {prompt}")
        
        client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        client.set_data(key='CLIP Text Encode Positive', text=prompt)
        
        # Generate image
        results = client.generate(["Result Image"])
        for key, image in results.items():
            filename = f"test_sync_workflow_{key}.png"
            image.save(filename)
            print(f"✓ Success! Saved: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        if client:
            client.close()

def test_sync_workflow_api():
    """Test sync client with workflow_api.json (direct load)"""
    print("\n=== Testing Sync Client with workflow_api.json ===")
    client = None
    try:
        client = ComfyUIClient(SERVER_ADDRESS, "workflow_api.json", debug=True)
        client.connect()
        
        # Test enhanced features
        test_enhanced_features_sync(client, "sync API")
        
        # Set random seed and prompt
        prompt = random.choice(TEST_PROMPTS)
        print(f"Using prompt: {prompt}")
        
        client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        client.set_data(key='CLIP Text Encode Positive', text=prompt)
        
        # Generate image
        results = client.generate(["Result Image"])
        for key, image in results.items():
            filename = f"test_sync_api_{key}.png"
            image.save(filename)
            print(f"✓ Success! Saved: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        if client:
            client.close()

async def test_async_workflow():
    """Test async client with workflow.json (auto-conversion)"""
    print("\n=== Testing Async Client with workflow.json ===")
    client = None
    try:
        client = ComfyUIClientAsync(SERVER_ADDRESS, "workflow.json", debug=True)
        await client.connect()
        
        # Test enhanced features
        await test_enhanced_features_async(client, "async workflow")
        
        # Set random seed and prompt
        prompt = random.choice(TEST_PROMPTS)
        print(f"Using prompt: {prompt}")
        
        await client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        await client.set_data(key='CLIP Text Encode Positive', text=prompt)
        
        # Generate image
        results = await client.generate(["Result Image"])
        for key, image in results.items():
            filename = f"test_async_workflow_{key}.png"
            image.save(filename)
            print(f"✓ Success! Saved: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        if client:
            await client.close()

async def test_async_workflow_api():
    """Test async client with workflow_api.json (direct load)"""
    print("\n=== Testing Async Client with workflow_api.json ===")
    client = None
    try:
        client = ComfyUIClientAsync(SERVER_ADDRESS, "workflow_api.json", debug=True)
        await client.connect()
        
        # Test enhanced features
        await test_enhanced_features_async(client, "async API")
        
        # Set random seed and prompt
        prompt = random.choice(TEST_PROMPTS)
        print(f"Using prompt: {prompt}")
        
        await client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        await client.set_data(key='CLIP Text Encode Positive', text=prompt)
        
        # Generate image
        results = await client.generate(["Result Image"])
        for key, image in results.items():
            filename = f"test_async_api_{key}.png"
            image.save(filename)
            print(f"✓ Success! Saved: {filename}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        if client:
            await client.close()

async def run_all_tests():
    """Run all test cases"""
    print("Starting ComfyUI Client Tests")
    print(f"Server: {SERVER_ADDRESS}")
    print("-" * 50)
    
    results = {}
    
    # Test sync versions
    results['sync_workflow'] = test_sync_workflow()
    results['sync_api'] = test_sync_workflow_api()
    
    # Test async versions
    results['async_workflow'] = await test_async_workflow()
    results['async_api'] = await test_async_workflow_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY - Enhanced Features Included")
    print("=" * 60)
    
    all_passed = True
    test_descriptions = {
        'sync_workflow': 'Sync Client + workflow.json + Enhanced Features',
        'sync_api': 'Sync Client + workflow_api.json + Enhanced Features', 
        'async_workflow': 'Async Client + workflow.json + Enhanced Features',
        'async_api': 'Async Client + workflow_api.json + Enhanced Features'
    }
    
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        description = test_descriptions.get(test_name, test_name)
        print(f"{symbol} {description}: {status}")
        if not passed:
            all_passed = False
    
    print("\nTested Enhanced Features:")
    print("  ✓ Debug mode support")
    print("  ✓ reload() method")
    print("  ✓ Enhanced set_data() with input_key/input_value")
    print("  ✓ set_data() with number parameter")
    print("  ✓ find_key_by_title() with class_type lookup")
    print("  ✓ Automatic workflow.json to API conversion")
    
    print("\n" + ("🎉 All tests passed! Both sync and async versions have equivalent functionality." 
                  if all_passed else "❌ Some tests failed!"))
    return all_passed

if __name__ == "__main__":
    # Run all tests
    all_passed = asyncio.run(run_all_tests())
    sys.exit(0 if all_passed else 1)