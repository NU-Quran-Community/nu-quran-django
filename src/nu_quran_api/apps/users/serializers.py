import typing as t

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    value: serializers.IntegerField = serializers.IntegerField(
        default=0,
    )

    class Meta:
        model = models.Category
        fields: str = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    category: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        default=1,
    )

    class Meta:
        model = models.Activity
        fields: t.Iterable = ("id", "category", "date")


class UserSerializer(serializers.ModelSerializer):
    username: serializers.CharField = serializers.CharField(trim_whitespace=True)
    referrer: serializers.SlugRelatedField = serializers.SlugRelatedField(
        queryset=models.User.objects.all(),
        slug_field="username",
        error_messages={
            "does_not_exist": "No referrer was found with the given username"
        },
        required=False,
        allow_null=True,
    )
    supervisor: serializers.SlugRelatedField = serializers.SlugRelatedField(
        queryset=models.User.objects.filter(groups__name="Supervisor"),
        slug_field="username",
        error_messages={
            "does_not_exist": "No supervisor was found with the given username"
        },
        required=False,
        allow_null=True,
    )
    groups: serializers.SlugRelatedField = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field="name",
        many=True,
        default=["Student"],
    )

    class Meta:
        model = models.User
        fields: t.Iterable[str] = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "referrer",
            "supervisor",
            "date_joined",
            "groups",
        )
        read_only_fields: t.Iterable[str] = ("date_joined",)
        extra_kwargs: dict = {"password": {"write_only": True}}

    def validate_username(self, value: str) -> str:
        if models.User.objects.filter(username__exact=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value

    def create(self, validated_data: dict) -> models.User:
        for i, grp in enumerate(validated_data["groups"]):
            validated_data["groups"][i] = Group.objects.get(name=grp)

        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserPointsSerializer(serializers.Serializer):
    user: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    points: serializers.IntegerField = serializers.IntegerField()
    activities: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.User
        fields: t.Iterable[str] = (
            "username",
            "activities",
            "points",
        )
