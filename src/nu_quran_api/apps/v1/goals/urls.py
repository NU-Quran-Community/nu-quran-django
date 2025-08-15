from rest_framework.routers import DefaultRouter
from .views import GoalViewSet
from django.urls import URLPattern, URLResolver, include, path

app_name: str = "goals"

router: DefaultRouter = DefaultRouter()
router.register("", GoalViewSet, basename="goal")
urlpatterns: list[URLPattern | URLResolver] = [path("", include(router.urls))]
