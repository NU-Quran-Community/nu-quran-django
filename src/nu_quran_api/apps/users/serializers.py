import typing as t

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
    category: CategorySerializer = CategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Activity
        fields: str = "__all__"


class UserSerializer(serializers.ModelSerializer):
    referrer: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    supervisor: serializers.SlugRelatedField = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = models.User
        fields: t.Iterable[str] = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "referrer",
            "supervisor",
        )
        read_only_fields: t.Iterable[str] = ("date_joined",)
