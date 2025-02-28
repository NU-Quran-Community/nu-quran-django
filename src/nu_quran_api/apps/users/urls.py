from django.urls import URLPattern, URLResolver, include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name: str = "users"

router: DefaultRouter = DefaultRouter()
router.register("", views.UserViewSet)
router.register(
    r"(?P<uid>\d+)/activities",
    views.UserActivitiesViewSet,
    basename="activity",
)

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),
]
