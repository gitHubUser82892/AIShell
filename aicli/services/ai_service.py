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
from openai import APIError as OpenAIAPIError
import re
from typing import Optional, Tuple, Union
from ..utils.exceptions import APIError

class AIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise APIError("API key is required")
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise APIError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def _clean_response(self, text: str) -> str:
        """Remove markdown code blocks and extra whitespace"""
        # Remove code block syntax
        text = re.sub(r'```\w*\n|```', '', text)
        # Remove extra whitespace
        text = text.strip()
        return text
    
    def get_command(self, query: str, explain: bool = False) -> Union[str, Tuple[str, str]]:
        """
        Get command suggestion from OpenAI
        
        Returns:
            Union[str, Tuple[str, str]]: Either just the command, or (command, explanation)
        """
        if not query:
            raise APIError("Query cannot be empty")

        try:
            if explain:
                system_message = (
                    "You are a Unix command line expert. Provide the command followed by "
                    "a detailed explanation. Format your response as: "
                    "COMMAND: <the command>\n"
                    "EXPLANATION: <detailed explanation of how the command works>"
                )
            else:
                system_message = (
                    "You are a Unix command line expert. "
                    "Provide only the command with no explanation or formatting."
                )

            response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=400 if explain else 200
            )
            
            if not response.choices:
                raise APIError("No response received from API")
            
            content = self._clean_response(response.choices[0].message.content)
            
            if explain:
                # Split response into command and explanation
                parts = content.split('\n', 1)
                if len(parts) == 2 and parts[0].startswith('COMMAND:'):
                    command = parts[0].replace('COMMAND:', '').strip()
                    explanation = parts[1].replace('EXPLANATION:', '').strip()
                    return command, explanation
                else:
                    raise APIError("Unexpected response format from AI")
            
            return content
            
        except OpenAIAPIError as e:
            raise APIError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise APIError(f"Unexpected error in AI service: {str(e)}") 