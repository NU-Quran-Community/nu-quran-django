import click
import uvicorn
from django.conf import settings
from django.core import management
from django.db.utils import IntegrityError

from ..asgi import application


def initialize_db() -> None:
    management.call_command("migrate")
    if len(settings.INIT_FIXTURES) > 0:
        try:
            management.call_command("loaddata", *settings.INIT_FIXTURES)
        except IntegrityError:
            pass


def initialize_roles() -> None:
    management.call_command("setuproles")


@click.command(
    "server",
    short_help="Start HTTP server",
    help="Start HTTP server for NU Quran API",
)
@click.help_option("-h", "--help")
@click.option(
    "-H",
    "--host",
    type=str,
    help="Listen address",
    default="0.0.0.0",
)
@click.option(
    "-p",
    "--port",
    type=int,
    help="Listen port",
    default=8000,
)
def server(host: str, port: int) -> None:
    initialize_db()
    initialize_roles()
    uvicorn.run(
        application,
        host=host,
        port=port,
        log_level="info",
    )
