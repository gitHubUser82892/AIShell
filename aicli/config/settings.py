"""
Settings Module

This module manages the application's configuration, handling both file-based
config and environment variables. It's configured to read from a custom keys file
in the user's home directory.

Configuration Hierarchy:
1. Custom keys file (~/.keys)
2. Environment variables (OPENAI_API_KEY)

File Format:
The keys file should be in YAML format and contain:
    openai_api_key_aishell: sk-...

Security Note:
    - The keys file should have restricted permissions (600)
    - Never commit API keys to version control
    - Keep the keys file in a secure location
"""

import yaml
import os
from pathlib import Path
from typing import Dict
from ..utils.exceptions import ConfigurationError

def load_config() -> Dict:
    """
    Load configuration from keys file or environment variables
    
    Returns:
        Dict: Configuration dictionary with API key
    
    Raises:
        ValueError: If no API key is found
        yaml.YAMLError: If the keys file is not valid YAML
    """
    try:
        home_dir = Path.home()
        keys_path = home_dir / '.keys'
        
        if keys_path.exists():
            try:
                with open(keys_path) as f:
                    keys_config = yaml.safe_load(f)
                    if not isinstance(keys_config, dict):
                        raise ConfigurationError("Invalid keys file format")
                    
                    api_key = keys_config.get('openai_api_key_aishell')
                    if api_key:
                        return {'openai_api_key': api_key}
            except yaml.YAMLError as e:
                raise ConfigurationError(f"Error parsing keys file: {str(e)}")
            except OSError as e:
                raise ConfigurationError(f"Error reading keys file: {str(e)}")
        
        # Fallback to environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ConfigurationError(
                f"OpenAI API key not found in {keys_path} or environment variables"
            )
        
        return {'openai_api_key': api_key}
        
    except Exception as e:
        raise ConfigurationError(f"Unexpected error loading config: {str(e)}") 