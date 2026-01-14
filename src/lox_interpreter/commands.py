import click


@click.command()
@click.argument("file", type=click.Path(exists=True), required=False)
def run(file):
    """
    Usage: lox [OPTIONS] FILENAME

    Execute the script FILENAME. If no FILENAME is passed, then open interactive LOX.

    FILENAME is the path of the file to check.
    """
    with open(file, "r") as f:
        source = f.read()
        click.echo(f"Running LOX script from {file}...")
