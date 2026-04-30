from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = _("Goals")

    class Scope(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        YEARLY = "yearly", _("Yearly")

    scope: models.CharField = models.CharField(
        _("scope"), max_length=10, choices=Scope.choices, default=Scope.MONTHLY
    )
    title: models.CharField = models.CharField(
        _("title"), max_length=255, blank=False, null=False
    )
    description: models.CharField = models.CharField(
        _("description"), max_length=255, blank=True, null=True
    )
    target: models.IntegerField = models.IntegerField(
        _("target"), validators=[MinValueValidator(0)]
    )
    current: models.IntegerField = models.IntegerField(
        _("current"), validators=[MinValueValidator(0)]
    )
    created_at: models.DateField = models.DateField(_("created at"), auto_now_add=True)
