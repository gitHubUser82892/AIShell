"""
Settings Module

This module manages the application's configuration, handling both file-based
config (YAML) and environment variables.

Configuration Hierarchy:
1. Local config file (~/.aicli/config.yaml)
2. Environment variables (OPENAI_API_KEY)

Configuration Options:
    - openai_api_key: API key for OpenAI services
    - (future) model: AI model to use
    - (future) temperature: AI response temperature
"""

import yaml
import os
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    """Load configuration from config file or environment variables"""
    config_path = Path.home() / '.aicli' / 'config.yaml'
    
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    
    # Fallback to environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment "
            "variable or create a config file at ~/.aicli/config.yaml"
        )
    
    return {
        'openai_api_key': api_key
    } 