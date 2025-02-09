import uvicorn
from django.conf import settings
from django.core import management

from ..asgi import application


def initialize_db() -> None:
    management.call_command("migrate")
    if len(settings.INIT_FIXTURES) > 0:
        management.call_command("loaddata", *settings.INIT_FIXTURES)


def run() -> None:
    initialize_db()
    uvicorn.run(application, host="0.0.0.0", port=8000, log_level="info")
