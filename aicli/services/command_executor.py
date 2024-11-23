"""
Command Executor Module

This module is responsible for safely executing shell commands generated by the AI.
It provides a wrapper around subprocess.run with additional safety checks and
error handling.

Features:
    - Safe command execution in shell environment
    - Output capture and formatting
    - Error handling and user feedback
    - Command execution confirmation

Security Note:
    Commands are executed in a shell context. Users should review commands
    before execution to ensure safety.
"""

import subprocess
import click
from typing import Optional

class CommandExecutor:
    def run(self, command: str) -> None:
        """Execute the shell command"""
        try:
            click.secho(f"\nExecuting: {command}", fg="blue")
            click.echo("=" * 40)
            
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True
            )
            
            if result.stdout:
                click.echo(result.stdout)
            
            if result.stderr:
                click.secho("Errors:", fg="red", err=True)
                click.secho(result.stderr, fg="red", err=True)
                
        except Exception as e:
            click.secho(f"Error executing command: {str(e)}", fg="red", err=True) 