import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nile_quran_community_api.settings")

application = get_asgi_application()
