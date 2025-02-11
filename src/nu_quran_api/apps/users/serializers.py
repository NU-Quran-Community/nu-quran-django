import typing as t

from rest_framework import serializers

from . import models


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
            "username",
            "email",
            "first_name",
            "last_name",
            "referrer",
            "supervisor",
        )
        read_only_fields: t.Iterable[str] = ("date_joined",)
