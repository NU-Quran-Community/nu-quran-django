from django.urls import URLPattern, URLResolver, path

from . import views

app_name: str = "users"

urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.ListUsersAPIView.as_view()),
]
