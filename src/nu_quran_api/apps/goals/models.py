from django.db import models
from django.core.validators import MinValueValidator


class Goal(models.Model):
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Goals"

    class Scope(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    scope = models.CharField(
        max_length=10, choices=Scope.choices, default=Scope.MONTHLY
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    target = models.IntegerField(validators=[MinValueValidator(0)])
    current = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
