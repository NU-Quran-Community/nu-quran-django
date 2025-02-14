from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from . import models


class CanModifyUser(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.User
    ) -> bool:
        if request.user and request.user.has_perm("change_user"):
            return True
        return obj == request.user


class CanDeleteUser(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.User
    ) -> bool:
        if request.user and request.user.has_perm("delete_user"):
            return True
        return obj == request.user
