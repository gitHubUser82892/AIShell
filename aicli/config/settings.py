"""
Settings Module

This module manages the application's configuration, handling both file-based
config and environment variables. It's configured to read from a custom keys file.

Configuration Hierarchy:
1. Custom keys file (/Users/rmayor/keys)
2. Environment variables (OPENAI_API_KEY)

File Format:
The keys file should be in YAML format and contain:
    openai_api_key_aishell: sk-...

Example keys file content:
    openai_api_key_aishell: sk-abcd1234...

Security Note:
    - The keys file should have restricted permissions (600)
    - Never commit API keys to version control
    - Keep the keys file in a secure location

Usage:
    from aicli.config.settings import load_config
    config = load_config()
    api_key = config['openai_api_key']

Error Handling:
    - Raises ValueError if API key is not found
    - Raises yaml.YAMLError if keys file is malformed
"""

import yaml
import os
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    """
    Load configuration from keys file or environment variables
    
    Returns:
        Dict: Configuration dictionary containing:
            - openai_api_key: The OpenAI API key for authentication
    
    Raises:
        ValueError: If no API key is found in keys file or environment
        yaml.YAMLError: If the keys file is not valid YAML
    
    Example:
        >>> config = load_config()
        >>> api_key = config['openai_api_key']
    """
    # Path to your keys file
    keys_path = Path('/Users/rmayor/keys')
    
    if keys_path.exists():
        with open(keys_path) as f:
            keys_config = yaml.safe_load(f)
            api_key = keys_config.get('openai_api_key_aishell')
            if api_key:
                return {'openai_api_key': api_key}
    
    # Fallback to environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please ensure it's properly set in "
            f"{keys_path} with key 'openai_api_key_aishell'"
        )
    
    return {
        'openai_api_key': api_key
    } 