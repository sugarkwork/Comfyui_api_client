# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modern Python packaging with pyproject.toml
- GitHub Actions CI/CD workflows
- Comprehensive test suite organization
- Development and test requirements files
- Code quality tool configurations (flake8, mypy, black)
- Documentation structure
- Contributing guidelines
- Code of Conduct
- Makefile for development automation
- Pre-commit configuration

## [0.1.0] - 2025-01-06

### Added
- Initial release of ComfyUI Client
- Synchronous client (`ComfyUIClient`)
- Asynchronous client (`ComfyUIClientAsync`)
- Automatic workflow format conversion
- Enhanced `set_data()` method for all parameter types
- Debug mode for development and troubleshooting
- Dynamic workflow reloading
- Comprehensive error handling
- Smart node lookup by title or class_type
- Direct image upload support
- Timeout handling for long-running operations
- Resource cleanup on connection close

### Features
- Support for both workflow.json and workflow_api.json formats
- Flexible parameter setting with various input types
- Image generation from specified nodes
- WebSocket-based communication with ComfyUI server
- Automatic retry mechanism for failed operations

[Unreleased]: https://github.com/sugarkwork/Comfyui_api_client/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sugarkwork/Comfyui_api_client/releases/tag/v0.1.0