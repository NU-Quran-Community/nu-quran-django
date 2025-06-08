from rest_framework import permissions


class CanCreateGoal(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user.is_authenticated):
            return False
        return request.user.groups.filter(name="Admin").exists()


class CanModifyGoal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Admin").exists()


class CanDeleteGoal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Admin").exists()
