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
