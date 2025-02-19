from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from . import models


class CanModifyUser(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.User
    ) -> bool:
        if request.user and request.user.has_perm("user.change_user"):
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
        if request.user and request.user.has_perm("user.delete_user"):
            return True
        return obj == request.user


class CanModifyActivity(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.Activity
    ) -> bool:
        if request.user and request.user.has_perm("user.change_activity"):
            if (
                request.user.groups.filter(name="Admin").exists()
                or obj.supervisor == request.user
            ):
                return True
        return obj.user == request.user


class CanDeleteActivity(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: models.Activity
    ) -> bool:
        if request.user and request.user.has_perm("activity.delete_activity"):
            # Admins and supervisors can delete activities
            if (
                request.user.groups.filter(name="Admin").exists()
                or obj.supervisor == request.user
            ):
                return True
        return obj.user == request.user
