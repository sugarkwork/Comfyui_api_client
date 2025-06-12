# ComfyUI Client Documentation

Welcome to the ComfyUI Client documentation. This library provides a Python interface for interacting with ComfyUI via its API.

## Quick Links

- [Installation](installation.md)
- [Quick Start Guide](quickstart.md)
- [API Reference](api.md)
- [Examples](examples.md)
- [Contributing](contributing.md)

## Features

- 🔄 **Dual Client Support**: Both sync and async implementations
- 🎯 **Automatic Format Detection**: Automatically converts workflows
- 🛠️ **Enhanced Configuration**: Flexible parameter setting
- 🐛 **Debug Mode**: Development and troubleshooting support
- 🔧 **Dynamic Reload**: Reload workflows without restarting
- 🛡️ **Robust Error Handling**: Comprehensive error messages
- 🔍 **Smart Node Lookup**: Find nodes by title or class_type
- 📦 **Image Upload Support**: Direct image upload to ComfyUI

## Getting Started

```python
from comfyuiclient import ComfyUIClient

# Initialize client
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