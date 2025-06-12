from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="comfyui-workflow-client",
    version="0.1.0",
    author="sugarkwork",
    description="A Python client for ComfyUI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sugarkwork/Comfyui_api_client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "aiohttp",
        "pillow",
    ],
    keywords="comfyui api client stable-diffusion",
    project_urls={
        "Bug Reports": "https://github.com/sugarkwork/Comfyui_api_client/issues",
        "Source": "https://github.com/sugarkwork/Comfyui_api_client",
    },
)