"""
AI-powered Command Line Interface (CLI) Tool

This module serves as the main entry point for the aicli application. It provides
a command-line interface for interacting with AI to generate and execute shell commands.

Key Components:
    - CLI command group and subcommands using Click
    - Integration with AI service for command generation
    - Command execution capabilities
    - History management

Usage:
    aicli ask "your command description"
    aicli ask -e "your command description"  # Execute immediately
    aicli ask -x "your command description"  # Get explanation
    aicli history                           # View command history

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required if not in config.yaml)

Configuration:
    ~/.aicli/config.yaml: Configuration file location
    ~/.aicli/history.json: Command history storage
"""

import click
from typing import Tuple
from .services.ai_service import AIService
from .services.command_executor import CommandExecutor
from .config.settings import load_config
from .utils.history_manager import HistoryManager

@click.group()
@click.pass_context
def cli(ctx):
    """AI-powered command line assistant"""
    ctx.ensure_object(dict)
    config = load_config()
    ctx.obj['config'] = config
    ctx.obj['ai_service'] = AIService(config['openai_api_key'])
    ctx.obj['history'] = HistoryManager()

@cli.command()
@click.argument('query', nargs=-1)
@click.option('--execute', '-e', is_flag=True, help='Execute the command directly')
@click.option('--explain', '-x', is_flag=True, help='Get explanation of the command')
@click.pass_context
def ask(ctx, query: Tuple[str], execute: bool, explain: bool):
    """Ask AI for a command based on your description"""
    query_text = ' '.join(query)
    ai_service = ctx.obj['ai_service']
    history = ctx.obj['history']

    try:
        # Get command from AI
        command = ai_service.get_command(query_text, explain)
        
        # Store in history
        history.add_command(query_text, command)

        # Display result
        if explain:
            click.echo("\nCommand explanation:")
            click.echo(command)
        else:
            click.secho("\nSuggested command:", fg="green")
            click.secho(command, fg="yellow")

            if execute:
                executor = CommandExecutor()
                executor.run(command)
            elif click.confirm('\nWould you like to execute this command?'):
                executor = CommandExecutor()
                executor.run(command)

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg="red", err=True)

@cli.command()
@click.pass_context
def history(ctx):
    """Show command history"""
    history = ctx.obj['history']
    commands = history.get_commands()
    
    if not commands:
        click.echo("No commands in history.")
        return

    click.echo("\nCommand History:")
    for i, (query, command) in enumerate(commands, 1):
        click.echo(f"\n{i}. Query: {query}")
        click.secho(f"   Command: {command}", fg="yellow")

if __name__ == '__main__':
    cli() 