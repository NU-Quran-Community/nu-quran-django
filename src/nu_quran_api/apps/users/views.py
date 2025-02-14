import typing as t

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
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
        elif self.action in ("delete"):
            permission_classes = [permissions.IsAuthenticated, userperms.CanDeleteUser]
        return [permission() for permission in permission_classes]


class UserActivitiesAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializers_classes = (
        serializers.ActivitySerializer,
        serializers.UserSerializer,
    )

    def get(self, request, id: int):
        user: models.User = models.User.objects.get(id=id)
        if user:
            activities: QuerySet[models.Activity] = models.Activity.objects.filter(
                user=user
            )
            serializer = serializers.ActivitySerializer(activities, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
