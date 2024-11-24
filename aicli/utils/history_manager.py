"""
History Manager Module

This module manages the command history functionality, storing and retrieving
past commands and their results.

Features:
    - JSON-based command history storage
    - Automatic history rotation (keeps last 100 commands)
    - Query and command pair storage
    - History file management

File Location:
    ~/.aicli/history.json

History Format:
    List of tuples containing (query, command) pairs
"""

import json
from pathlib import Path
from typing import List, Tuple
from .exceptions import HistoryError

class HistoryManager:
    def __init__(self):
        try:
            self.history_file = Path.home() / '.aicli' / 'history.json'
            self.history_file.parent.mkdir(exist_ok=True)
        except Exception as e:
            raise HistoryError(f"Failed to initialize history manager: {str(e)}")

    def add_command(self, query: str, command: str) -> None:
        """Add a command to history"""
        if not query or not command:
            raise HistoryError("Query and command are required")

        try:
            history = self.get_history()
            history.append((query, command))
            
            # Keep only last 100 commands
            history = history[-100:]
            
            self.history_file.write_text(
                json.dumps(history, indent=2),
                encoding='utf-8'
            )
        except Exception as e:
            raise HistoryError(f"Failed to add command to history: {str(e)}")

    def get_history(self) -> List[Tuple[str, str]]:
        """Get command history"""
        try:
            if self.history_file.exists():
                history = json.loads(self.history_file.read_text(encoding='utf-8'))
                return history if isinstance(history, list) else []
            return []
        except json.JSONDecodeError as e:
            raise HistoryError(f"Invalid history file format: {str(e)}")
        except Exception as e:
            raise HistoryError(f"Failed to read history: {str(e)}") 