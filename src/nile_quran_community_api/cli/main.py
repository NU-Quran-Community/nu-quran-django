import click

from .server import server


@click.group()
@click.help_option("--help", "-h")
def main():
    pass


main.add_command(server)
