from rest_framework.serializers import ModelSerializer, ValidationError
from models import Goal


class GoalSerializer(ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"

    def validate(self, data):
        if data["current"] > data["target"]:
            raise ValidationError("Current is greater than target")
        return data
