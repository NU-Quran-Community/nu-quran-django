from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView

from . import APPS

urlpatterns: list[URLPattern | URLResolver] = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

# NOTE: Dynamically add URLs for all apps under v1 module
urlpatterns += [path(f"{app.split('.')[-1]}/", include(f"{app}.urls")) for app in APPS]
