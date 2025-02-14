from django.urls import URLPattern, URLResolver, path

from . import views

app_name: str = "users"

urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.ListUsersAPIView.as_view(), name="users_list"),
    path("<int:id>/", views.UserAPIView.as_view(), name="user_id"),
    path(
        "<int:id>/activities/",
        views.UserActivitiesAPIView.as_view(),
        name="user_activities",
    ),
]
