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

class HistoryManager:
    def __init__(self):
        self.history_file = Path.home() / '.aicli' / 'history.json'
        self.history_file.parent.mkdir(exist_ok=True)
        
        if not self.history_file.exists():
            self.history_file.write_text('[]')
    
    def add_command(self, query: str, command: str) -> None:
        """Add a command to history"""
        history = self._load_history()
        history.append((query, command))
        
        # Keep only last 100 commands
        history = history[-100:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f)
    
    def get_commands(self) -> List[Tuple[str, str]]:
        """Get command history"""
        return self._load_history()
    
    def _load_history(self) -> List[Tuple[str, str]]:
        """Load history from file"""
        try:
            with open(self.history_file) as f:
                return json.load(f)
        except Exception:
            return [] 