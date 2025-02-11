from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class ListUsersAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request) -> Response:
        users: QuerySet = models.User.objects.all()
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            users, many=True
        )
        return Response(data=serializer.data)
