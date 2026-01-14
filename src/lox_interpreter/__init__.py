import click

import lox_interpreter.commands as commands


@click.group()
def main():
    """Entry point for the Lox Interpreter CLI."""


main.add_command(commands.run)

if __name__ == "__main__":
    main()
