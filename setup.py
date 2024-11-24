"""
Copyright (c) 2024 Ryan Mayor
Licensed under the MIT License. See LICENSE file in the project root for full license information.

AICLI - AI-powered Command Line Assistant

A command-line tool that uses OpenAI to help generate and execute shell commands.
This tool helps users by converting natural language descriptions into shell commands.

Example:
    $ aicli ask "list all python files modified today"
    $ aicli ask -e "find large files over 100MB"
"""

from setuptools import setup, find_packages

setup(
    name="aicli",
    version="0.1.0",
    description="AI-powered command line assistant",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
        "openai>=1.12.0",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        'console_scripts': [
            'aicli=aicli.main:cli',
        ],
    },
) 