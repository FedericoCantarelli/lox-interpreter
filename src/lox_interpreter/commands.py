"""Commands for the Lox Interpreter CLI tool."""

import click

from lox_interpreter.lox.runner import Runner


@click.command()
@click.argument("file", type=click.Path(exists=True), required=False, default=None)
def run(file):
    """
    Usage: lox run [OPTIONS] FILENAME

    Execute the script FILENAME. If no FILENAME is passed, then open interactive LOX.

    FILENAME is the path of the file to check.
    """
    runner = Runner()
    if file is None:
        runner.run_repl()
    else:
        runner.run_file(file)
