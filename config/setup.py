#!/usr/bin/env python3
"""
Setup script for Read2Me
"""

import os
from setuptools import setup, find_packages

# Get paths relative to setup.py location
setup_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(setup_dir)

with open(os.path.join(root_dir, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(os.path.join(setup_dir, "requirements_simple.txt"), "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="read2me",
    version="1.0.0",
    author="Your Name",
    description="Simple CLI and library for generating audiobooks from text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where=os.path.join(root_dir, "src")),
    package_dir={"": os.path.join(root_dir, "src")},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "read2me=read2me.cli.read2me_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)