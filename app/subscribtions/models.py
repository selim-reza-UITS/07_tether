from django.db import models
from shortuuid.django_fields import ShortUUIDField

class Subscription(models.Model):
    class PackageType(models.TextChoices):
        FREE = "FREE", "Free"
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"

    package_id = ShortUUIDField(
        length=6,
        alphabet="1234567890abcdefghijklmnopqrstuvwxyz",
        primary_key=True,
        editable=False
    )
    package_amount = models.PositiveIntegerField(default=0)
    package_type = models.CharField(
        max_length=10,
        choices=PackageType.choices,
        default=PackageType.FREE
    )
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.package_type} ({self.package_amount})"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created_at"]
