import click

from tools import commands


@click.group()
def main():
    """Entry point for the AST Tool CLI."""


main.add_command(commands.ast)

if __name__ == "__main__":
    main()
