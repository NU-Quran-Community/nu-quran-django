import typing as t

from django.db.models import QuerySet, Sum
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

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


class UserPointsView(generics.ListAPIView):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.UserPointsSerializer
    filterset_class = filters.ActivitiesFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Ordering",
                many=True,
                type=str,
                enum=("points", "-points"),
                required=False,
            )
        ]
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        response_data: list[dict] = []
        activities = self.filter_queryset(self.get_queryset())
        users = models.User.objects.all()

        for user in users:
            acts: QuerySet[models.Activity] = activities.filter(user=user)
            points = acts.aggregate(Sum("category__value"))["category__value__sum"] or 0
            response_data.append(
                {
                    "user": user,
                    "points": points,
                    "activities": acts,
                }
            )

        # NOTE: sort response data based on the defined ordering fields
        ordering: list[str] = request.GET.get("ordering", "").split(",")
        sorted_data = response_data
        for field in ("points",):
            if field in ordering or f"-{field}" in ordering:
                sorted_data = sorted(
                    sorted_data,
                    key=lambda x: x[field],
                    reverse=(f"-{field}" in ordering),
                )

        page = self.paginate_queryset(sorted_data)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(sorted_data, many=True)
        return Response(serializer.data)
