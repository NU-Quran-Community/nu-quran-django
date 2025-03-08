import typing as t

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets
from rest_framework.exceptions import NotFound

from . import filters, models
from . import permissions as userperms
from . import serializers


@extend_schema_view(create=extend_schema(auth=[]))
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter

    def get_permissions(self) -> t.Sequence[permissions.BasePermission]:
        permission_classes: t.Sequence[type[permissions.BasePermission]] = []
        if self.action == "create":
            permission_classes = [userperms.CanCreateUser]
        elif self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ("update", "partial_update"):
            permission_classes = [permissions.IsAuthenticated, userperms.CanModifyUser]
        elif self.action == "destroy":
            permission_classes = [permissions.IsAuthenticated, userperms.CanDeleteUser]
        return [permission() for permission in permission_classes]


class UserActivitiesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActivitySerializer
    filterset_class = filters.UserActivitiesFilter

    def get_user(self) -> models.User:
        uid: t.Optional[int] = self.kwargs.get("uid")
        user = models.User.objects.filter(id=uid).first()
        if not user:
            raise NotFound(detail="No user was found with the given ID.")
        return user

    def get_permissions(self) -> t.Sequence[permissions.BasePermission]:
        permission_classes: t.Sequence[type[permissions.BasePermission]] = []
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ("create", "update", "partial_update"):
            permission_classes = [
                permissions.IsAuthenticated,
                userperms.CanModifyActivity,
            ]
        elif self.action == "destroy":
            permission_classes = [
                permissions.IsAuthenticated,
                userperms.CanModifyActivity,
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self) -> QuerySet[models.Activity]:
        if getattr(self, "swagger_fake_view", False):
            return models.Activity.objects.none()

        user: models.User = self.get_user()
        return user.activities.all()

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.get_user())

    def perform_update(self, serializer) -> None:
        serializer.save(user=self.get_user())
