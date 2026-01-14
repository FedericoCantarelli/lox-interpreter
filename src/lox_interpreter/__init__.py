"""Lox Interpreter CLI entry point."""

import click

from lox_interpreter import commands


@click.group()
def main():
    """Entry point for the Lox Interpreter CLI."""


main.add_command(commands.run)

if __name__ == "__main__":
    main()
