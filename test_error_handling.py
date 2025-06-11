#!/usr/bin/env python3
"""Test error handling improvements"""

import asyncio
from comfyuiclient import ComfyUIClient, ComfyUIClientAsync

def test_error_handling():
    """Test various error conditions"""
    print("=== Testing Error Handling ===\n")
    
    # Test with invalid server
    print("1. Testing connection to invalid server:")
    try:
        client = ComfyUIClient("invalid-server:8188", "workflow_api.json", debug=True)
        client.connect()
        client.queue_prompt({})
        print("  ✗ Should have raised ConnectionError")
    except ConnectionError as e:
        print(f"  ✓ Caught expected ConnectionError: {e}")
    except Exception as e:
        print(f"  ⚠ Unexpected error: {e}")
    
    # Test with missing file
    print("\n2. Testing missing workflow file:")
    try:
        client = ComfyUIClient("localhost:8188", "nonexistent.json", debug=True)
        print("  ✗ Should have raised FileNotFoundError")
    except FileNotFoundError:
        print("  ✓ Caught expected FileNotFoundError")
    except Exception as e:
        print(f"  ✓ Handled file error gracefully: {e}")
    
    # Test with invalid JSON
    print("\n3. Testing invalid JSON file:")
    with open("invalid.json", "w") as f:
        f.write("{ invalid json")
    
    try:
        client = ComfyUIClient("localhost:8188", "invalid.json", debug=True)
        print("  ✗ Should have raised JSON error")
    except Exception as e:
        print(f"  ✓ Handled JSON error gracefully: {e}")
    
    # Test find_key_by_title with non-existent key
    print("\n4. Testing non-existent key lookup:")
    try:
        client = ComfyUIClient("localhost:8188", "workflow_api.json", debug=False)
        result = client.find_key_by_title("NonExistentNode")
        if result is None:
            print("  ✓ Returns None for non-existent key (no debug output)")
        else:
            print(f"  ✗ Expected None, got: {result}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
    
    # Test with debug mode
    print("\n5. Testing non-existent key lookup with debug:")
    try:
        client = ComfyUIClient("localhost:8188", "workflow_api.json", debug=True)
        result = client.find_key_by_title("NonExistentNode")
        if result is None:
            print("  ✓ Returns None for non-existent key (with debug output)")
        else:
            print(f"  ✗ Expected None, got: {result}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
    
    print("\n✓ Error handling tests completed!")

async def test_async_error_handling():
    """Test async error handling"""
    print("\n=== Testing Async Error Handling ===\n")
    
    # Test async connection to invalid server
    print("1. Testing async connection to invalid server:")
    client = None
    try:
        client = ComfyUIClientAsync("invalid-server:8188", "workflow_api.json", debug=True)
        await client.connect()
        print("  ✗ Should have raised ConnectionError")
    except ConnectionError as e:
        print(f"  ✓ Caught expected ConnectionError: {e}")
    except Exception as e:
        print(f"  ⚠ Unexpected error: {e}")
    finally:
        if client:
            try:
                await client.close()
            except:
                pass
    
    print("\n✓ Async error handling tests completed!")

async def main():
    test_error_handling()
    await test_async_error_handling()
    
    # Cleanup
    import os
    try:
        os.remove("invalid.json")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())