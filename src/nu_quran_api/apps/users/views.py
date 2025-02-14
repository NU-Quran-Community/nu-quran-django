from django.db.models import QuerySet
from rest_framework import permissions, pagination, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class ListUsersAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination

    def get(self, request: Request) -> Response:
        users: QuerySet = models.User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            paginated_users, many=True
        )
        return paginator.get_paginated_response(serializer.data)


class UserAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request: Request, id: int) -> Response:
        user: models.User = models.User.objects.get(id=id)
        serializer: serializers.UserSerializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def post(self, request: Request, id: int) -> Response:
        user: models.User = models.User.objects.get(id=id)
        serializer: serializers.UserSerializer = serializers.UserSerializer(
            user, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id: int) -> Response:
        if request.user.has_perm("delete_user"):
            user: models.User = models.User.objects.get(id=id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "You do not have permission to delete this user"},
                status=status.HTTP_403_FORBIDDEN,
            )


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
