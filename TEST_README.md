# ComfyUI Client Test Suite

This directory contains comprehensive tests for the ComfyUIClient library, which tests both synchronous and asynchronous versions with different workflow formats.

## Test Files

### `test_comfyui_client.py`
A comprehensive test script that validates:
- Format conversion from workflow.json to API format
- Automatic format detection
- All 4 client/format combinations
- Server connectivity
- Image generation

### `demo_usage.py`
A simpler demo script showing practical usage examples for all 4 combinations.

## Running the Tests

### Prerequisites
1. Ensure ComfyUI server is running
2. Update `SERVER_ADDRESS` in both test scripts to match your server
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run Comprehensive Tests
```bash
python test_comfyui_client.py
```

This will:
- Test format conversion functionality
- Test sync client with workflow.json (auto-conversion)
- Test sync client with workflow_api.json (direct load)
- Test async client with workflow.json (auto-conversion)
- Test async client with workflow_api.json (direct load)
- Generate test images for each successful combination
- Display a summary of all test results

### Run Demo Script
```bash
python demo_usage.py
```

This will generate 4 demo images using different prompts for each combination.

## Test Output

The test script provides color-coded output:
- ✓ Green: Successful operations
- ✗ Red: Failed operations
- ℹ Blue: Information messages
- ⚠ Yellow: Warnings

## Expected Behavior

### Format Detection
- **workflow.json**: Contains `nodes` and `links` arrays, automatically converted to API format
- **workflow_api.json**: Already in API format, loaded directly without conversion

### Generated Files
After successful test runs, you should see:
- `test_sync_workflow.png`
- `test_sync_workflow_api.png`
- `test_async_workflow.png`
- `test_async_workflow_api.png`

And from the demo script:
- `demo_sync_workflow.png`
- `demo_sync_api.png`
- `demo_async_workflow.png`
- `demo_async_api.png`

## Troubleshooting

### Server Connection Failed
- Ensure ComfyUI is running
- Check the SERVER_ADDRESS in the test scripts
- Verify firewall settings

### Node Not Found Errors
- The workflow files may use different node names
- Check the node titles in your workflow files
- Common variations: "CLIP Text Encode Positive", "CLIPTextEncode", "positive"

### Missing Dependencies
```bash
pip install requests aiohttp pillow
```