#!/usr/bin/env python3
"""
Demo script showing practical usage of ComfyUIClient
"""

import random
import sys
import asyncio
from comfyuiclient import ComfyUIClient, ComfyUIClientAsync

# Configuration - Update this to your ComfyUI server
SERVER_ADDRESS = "192.168.1.27:8188"


def demo_sync_workflow_json():
    """Demo using sync client with workflow.json (auto-conversion)"""
    print("\n--- Sync Client with workflow.json ---")
    
    client = ComfyUIClient(SERVER_ADDRESS, "workflow.json")
    client.connect()
    
    try:
        # Set a random seed
        client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        
        # Set prompt
        client.set_data(key='CLIP Text Encode Positive', text="a majestic eagle soaring through clouds")
        
        # Generate and save
        results = client.generate(["Result Image"])
        for key, image in results.items():
            filename = "demo_sync_workflow.png"
            image.save(filename)
            print(f"Saved: {filename}")
            
    finally:
        client.close()


def demo_sync_api_json():
    """Demo using sync client with workflow_api.json (direct load)"""
    print("\n--- Sync Client with workflow_api.json ---")
    
    client = ComfyUIClient(SERVER_ADDRESS, "workflow_api.json")
    client.connect()
    
    try:
        # Set a random seed
        client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        
        # Set prompt
        client.set_data(key='CLIP Text Encode Positive', text="a futuristic cityscape at night")
        
        # Generate and save
        results = client.generate(["Result Image"])
        for key, image in results.items():
            filename = "demo_sync_api.png"
            image.save(filename)
            print(f"Saved: {filename}")
            
    finally:
        client.close()


async def demo_async_workflow_json():
    """Demo using async client with workflow.json (auto-conversion)"""
    print("\n--- Async Client with workflow.json ---")
    
    client = ComfyUIClientAsync(SERVER_ADDRESS, "workflow.json")
    await client.connect()
    
    try:
        # Set a random seed
        await client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        
        # Set prompt
        await client.set_data(key='CLIP Text Encode Positive', text="a serene Japanese garden in autumn")
        
        # Generate and save
        results = await client.generate(["Result Image"])
        for key, image in results.items():
            filename = "demo_async_workflow.png"
            image.save(filename)
            print(f"Saved: {filename}")
            
    finally:
        await client.close()


async def demo_async_api_json():
    """Demo using async client with workflow_api.json (direct load)"""
    print("\n--- Async Client with workflow_api.json ---")
    
    client = ComfyUIClientAsync(SERVER_ADDRESS, "workflow_api.json")
    await client.connect()
    
    try:
        # Set a random seed
        await client.set_data(key='KSampler', seed=random.randint(0, sys.maxsize))
        
        # Set prompt
        await client.set_data(key='CLIP Text Encode Positive', text="a magical forest with glowing mushrooms")
        
        # Generate and save
        results = await client.generate(["Result Image"])
        for key, image in results.items():
            filename = "demo_async_api.png"
            image.save(filename)
            print(f"Saved: {filename}")
            
    finally:
        await client.close()


async def main():
    """Run all demos"""
    print("ComfyUI Client Demo - All 4 Combinations")
    print("=" * 50)
    
    # Sync demos
    demo_sync_workflow_json()
    demo_sync_api_json()
    
    # Async demos
    await demo_async_workflow_json()
    await demo_async_api_json()
    
    print("\n" + "=" * 50)
    print("All demos completed!")
    print("\nGenerated files:")
    print("  - demo_sync_workflow.png")
    print("  - demo_sync_api.png")
    print("  - demo_async_workflow.png")
    print("  - demo_async_api.png")


if __name__ == "__main__":
    asyncio.run(main())