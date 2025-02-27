from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from . import models


class CanModifyUser(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.User
    ) -> bool:
        if request.user and request.user.has_perm("users.change_user"):
            # NOTE: only admins can edit the following fields of a user:
            # - referrer
            # - supervisor
            # - groups
            if any(
                field in request.data for field in ("referrer", "supervisor", "groups")
            ):
                return request.user.groups.filter(name="Admin").exists()
            else:
                return True
        return obj == request.user


class CanDeleteUser(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.User
    ) -> bool:
        if request.user and request.user.has_perm("users.delete_user"):
            return True
        return obj == request.user


class CanModifyActivity(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.Activity
    ) -> bool:
        # Allow admins and supervisors to modify activities
        if request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Supervisor"]).exists()
        return False


class CanDeleteActivity(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.Activity
    ) -> bool:
        # Allow admins and supervisors to delete activities
        if request.user.is_authenticated:
            return request.user.groups.filter(name__in=["Admin", "Supervisor"]).exists()
        return False
