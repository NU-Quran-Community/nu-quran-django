import typing as t

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        permissions: t.Iterable[tuple[str, str]] = (
            ("change_user_activities", "Can change the user's activities"),
        )

    referrer: models.ForeignKey = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="User referrer reference.",
        related_name="referred",
    )
    supervisor: models.ForeignKey = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="User supervisor reference (required for students).",
        related_name="supervised",
    )


class Category(models.Model):
    name: models.CharField = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True,
    )
    value: models.IntegerField = models.IntegerField(
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return self.name


class Activity(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    date: models.DateTimeField = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"{self.user} - {self.category} - {self.date}"
