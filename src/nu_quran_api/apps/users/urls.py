from django.urls import URLPattern, URLResolver, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name: str = "users"

urlpatterns: list[URLPattern | URLResolver] = [
    path("auth/", TokenObtainPairView.as_view(), name="authtoken"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="authtoken-refresh"),
]
