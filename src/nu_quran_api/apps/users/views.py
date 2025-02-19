import typing as t

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import permissions as userperms
from . import serializers


@extend_schema_view(create=extend_schema(auth=[]))
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self) -> t.Sequence[permissions.BasePermission]:
        permission_classes: t.Sequence[type[permissions.BasePermission]] = []
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ("update", "partial_update"):
            permission_classes = [permissions.IsAuthenticated, userperms.CanModifyUser]
        elif self.action == "destroy":
            permission_classes = [permissions.IsAuthenticated, userperms.CanDeleteUser]
        return [permission() for permission in permission_classes]

    def create(self, request: Request, *args, **kwargs) -> Response:
        if "groups" in request.data:
            raise PermissionDenied("Insufficient permissions to set user groups")
        return super().create(request, *args, **kwargs)


class UserActivitiesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Activity.objects.all()
    serializers_classes = serializers.ActivitySerializer

    def get_permissions(self) -> t.Sequence[permissions.BasePermission]:
        permission_classes: t.Sequence[type[permissions.BasePermission]] = []
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ("update", "partial_update"):
            permission_classes = [
                permissions.IsAuthenticated,
                userperms.CanModifyActivity,
            ]
        elif self.action == "destroy":
            permission_classes = [
                permissions.IsAuthenticated,
                userperms.CanDeleteActivity,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        if user_id:
            return self.queryset.filter(user_id=user_id)
        return self.queryset

    def perform_create(self, serializer):
        user_id = self.kwargs["user"]
        serializer.save(user_id=user_id)
