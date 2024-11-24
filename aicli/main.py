"""
Main CLI Module
"""
import click
from typing import Tuple
from .services.ai_service import AIService
from .services.command_executor import CommandExecutor
from .config.settings import load_config
from .utils.history_manager import HistoryManager
from .utils.exceptions import (
    AICLIError,
    ConfigurationError,
    APIError,
    CommandExecutionError,
    HistoryError
)

def init_services() -> Tuple[AIService, CommandExecutor, HistoryManager]:
    """Initialize all services"""
    try:
        config = load_config()
        return (
            AIService(config['openai_api_key']),
            CommandExecutor(),
            HistoryManager()
        )
    except Exception as e:
        raise ConfigurationError(f"Failed to initialize services: {str(e)}")

@click.group()
def cli():
    """AI-powered command line assistant that converts natural language to shell commands.

    Basic Usage:
        aicli ask "your command description"    Generate a command
        aicli ask -x "your description"         Get command with explanation
        aicli ask -e "your description"         Generate and execute immediately
        aicli history                          Show command history

    Examples:
        aicli ask "find all pdf files"
        aicli ask -x "list large files over 100MB"
        aicli ask -e "show disk usage in human readable format"
    """
    pass

@cli.command()
@click.argument('query')
@click.option('-x', '--explain', is_flag=True, help='Get detailed explanation of how the command works')
@click.option('-e', '--execute', is_flag=True, help='Execute the command immediately without confirmation')
def ask(query: str, explain: bool, execute: bool):
    """Convert natural language description into shell command.

    Arguments:
        QUERY    Your description of what you want to do

    Options:
        -x, --explain     Show detailed explanation of how the command works
        -e, --execute     Execute the command immediately without confirmation

    Examples:
        aicli ask "list files by size"              Simple command generation
        aicli ask -x "find duplicate files"         Get command with explanation
        aicli ask -e "show system information"      Generate and execute immediately
        aicli ask -x -e "compress all jpg files"    Explain and execute
    """
    try:
        ai_service, cmd_executor, history = init_services()
        
        # Get command from AI
        result = ai_service.get_command(query, explain)
        
        if explain:
            command, explanation = result
            click.echo("\nSuggested command:")
            click.echo(command)
            click.echo("\nExplanation:")
            click.echo(explanation)
            click.echo()
        else:
            command = result
            click.echo("\nSuggested command:")
            click.echo(command)
            click.echo()
        
        # Add to history (only the command, not the explanation)
        if not explain:
            history.add_command(query, command)
        
        # Execute if requested or confirmed
        if execute:
            cmd_executor.run(command)
        else:
            if click.confirm("Would you like to execute this command?"):
                cmd_executor.run(command)
                
    except AICLIError as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)
        exit(1)
    except Exception as e:
        click.secho(f"Unexpected error: {str(e)}", fg="red", err=True)
        exit(1)

@cli.command()
def history():
    """Show command history"""
    try:
        _, _, history_manager = init_services()
        history = history_manager.get_history()
        
        if not history:
            click.echo("No command history found.")
            return
            
        click.echo("\nCommand History:")
        for i, (query, cmd) in enumerate(history, 1):
            click.echo(f"\n{i}. Query: {query}")
            click.echo(f"   Command: {cmd}")
            
    except AICLIError as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)
        exit(1)
    except Exception as e:
        click.secho(f"Unexpected error: {str(e)}", fg="red", err=True)
        exit(1)

if __name__ == '__main__':
    cli() 