"""
Copyright (c) 2024 Ryan Mayor
Licensed under the MIT License. See LICENSE file in the project root for full license information.

AI Service Module: Handles communication with OpenAI API and command generation.
"""

# AI Shell Command Assistant

An AI-powered command-line tool that helps generate and execute shell commands from natural language descriptions. This tool uses OpenAI's GPT-4 to convert plain English descriptions into executable shell commands.

## Features

- Convert natural language to shell commands
- Execute commands directly
- Get detailed explanations of commands
- Command history tracking
- Interactive command confirmation

## Installation

1. Clone the repository:
git clone https://github.com/ryanmayor/AIShell.git
cd AIShell

2. Install the package:
pip install -e .

3. Configure your OpenAI API key in `/Users/[username]/keys`:
```yaml
openai_api_key_aishell: your-api-key-here
```

## Usage

### Basic Command Generation
```bash
aicli ask "list files in current directory ordered by size"
```

### Get Command Explanation
```bash
aicli ask -x "find all python files modified in the last 24 hours"
```

### Execute Command Directly
```bash
aicli ask -e "show disk usage in human readable format"
```

### View Command History
```bash
aicli history
```

## Examples

Here are some example commands you can try:

- `aicli ask "find large files over 100MB"`
- `aicli ask "search all python files for the text 'openai'"`
- `aicli ask "compress all jpg files in current directory"`
- `aicli ask -x "find duplicate files"` (includes explanation)

## Technical Details

- Uses OpenAI's GPT-4-1106-preview model
- Built with Python's Click framework for CLI
- Supports Unix/Linux shell commands
- Includes safety checks before command execution

## Requirements

- Python 3.8 or higher
- OpenAI API key with active billing
- Unix-like environment (macOS, Linux)

## Project Structure
```plaintext
AIShell/
├── setup.py                    # Package configuration, dependencies, and CLI entry point
├── README.md                   # Project documentation and usage guide
├── aicli/                      # Main package directory
│   ├── __init__.py            # Package initialization and version info
│   ├── main.py                # CLI command definitions and argument parsing
│   │                          # Handles user interaction and command flow
│   │                          # - Initializes all services and utilities
│   │                          # - Manages command-line interface using Click
│   │                          # - Coordinates between AI service and command execution
│   │
│   ├── services/              # Core services directory
│   │   ├── __init__.py        # Services initialization
│   │   ├── ai_service.py      # OpenAI API integration:
│   │   │                      # - Manages API communication
│   │   │                      # - Formats prompts for command generation
│   │   │                      # - Handles model responses and errors
│   │   │                      # - Uses GPT-4-1106-preview for optimal results
│   │   │
│   │   └── command_executor.py # Safe shell command execution:
│   │                          # - Validates commands before execution
│   │                          # - Handles command output formatting
│   │                          # - Manages error reporting
│   │                          # - Provides execution confirmation
│   │
│   ├── config/                # Configuration directory
│   │   ├── __init__.py        # Config initialization
│   │   └── settings.py        # Configuration management:
│   │                          # - Loads API keys from user's keys file
│   │                          # - Manages environment variables
│   │                          # - Handles configuration errors
│   │
│   └── utils/                 # Utilities directory
│       ├── __init__.py        # Utils initialization
│       └── history_manager.py # Command history management:
│                             # - Stores command history in JSON format
│                             # - Manages history file I/O
│                             # - Implements history rotation
│                             # - Provides history search and retrieval

Component Interaction Flow:
1. User Input Flow:
   - main.py receives user command through Click interface
   - Passes natural language query to ai_service.py
   - Receives generated shell command
   - Optionally sends command to command_executor.py

2. Configuration Flow:
   - settings.py loads API key on startup
   - Provides configuration to ai_service.py
   - Manages persistent settings across sessions

3. Command Processing:
   - ai_service.py generates shell commands
   - command_executor.py handles execution
   - history_manager.py records all interactions

4. History Management:
   - Automatically saves successful commands
   - Provides command retrieval functionality
   - Maintains user interaction history
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ No liability
- ⚠️ No warranty

The MIT License is a permissive license that allows you to do anything with the code as long as you include the original copyright and license notice in any copy of the software/source.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


