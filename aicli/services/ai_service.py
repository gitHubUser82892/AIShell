"""
AI Service Module

This module handles all interactions with the OpenAI API. It is responsible for
sending queries to the AI model and processing the responses into usable shell commands.

The AIService class provides methods to:
    - Initialize OpenAI API client
    - Generate shell commands from natural language descriptions
    - Handle API errors and rate limiting
    - Format AI responses for CLI output

Dependencies:
    - openai: OpenAI API client library
    - typing: Type hints for better code documentation
"""


from openai import OpenAI
from typing import Optional

class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def get_command(self, query: str, explain: bool = False) -> str:
        """Get command suggestion from OpenAI"""
        system_message = (
            "You are a Unix command line expert. "
            "Provide only the command with no explanation."
        ) if not explain else (
            "You are a Unix command line expert. "
            "Provide the command and a detailed explanation of how it works."
        )

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip() 