from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Role(models.Model):
    name: models.CharField = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )


class User(AbstractUser):
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
    is_active: models.BooleanField = models.BooleanField(
        "active",
        default=False,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )
    roles: models.ManyToManyField = models.ManyToManyField(Role, related_name="users")

    def clean(self, *args, **kwargs) -> None:
        if (
            self.supervisor
            and not self.supervisor.roles.filter(name__iexact="supervisor").exists()
        ):
            raise ValidationError("Selected user has insufficient roles")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)
