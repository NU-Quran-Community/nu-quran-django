from rest_framework import viewsets, permissions
from .serializers import GoalSerializer
from .permissions import CanCreateGoal, CanDeleteGoal, CanModifyGoal
from .models import Goal


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_permissions(self):
        permission_classes: list[permissions.BasePermission] = []
        if self.action in ("list", "retrieve"):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "create":
            permission_classes = [CanCreateGoal]
        elif self.action in ("update", "partial_update"):
            permission_classes = [CanModifyGoal]
        elif self.action == "delete":
            permission_classes = [CanDeleteGoal]
        return [permission() for permission in permission_classes]
