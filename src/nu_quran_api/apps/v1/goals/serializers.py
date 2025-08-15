from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Goal


class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"

    def validate(self, data):
        current = data.get("current")
        target = data.get("target")
        if current is not None and target is not None:
            if current > target:
                raise ValidationError("Current is greater than target")

        return data
