from django.urls import URLPattern, URLResolver, include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name: str = "users"

router: DefaultRouter = DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),
    path("<int:pk>/activities/", views.UserActivitiesAPIView.as_view()),
]
