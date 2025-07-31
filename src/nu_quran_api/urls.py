from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(), name="docs"),
    path("auth/", TokenObtainPairView.as_view(), name="authtoken"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="authtoken-refresh"),
    path("users/", include("nu_quran_api.apps.users.urls")),
    path("goals/", include("nu_quran_api.apps.goals.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
