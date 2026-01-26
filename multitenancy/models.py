# multitenancy/models.py
from django.conf import settings
from django.db import models

from .thread_local import get_current_user


class TenantManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        qs = super().get_queryset()
        # Jeśli mamy użytkownika, filtrujemy wszystko pod niego
        if user:
            return qs.filter(user=user)
        return qs


class TenantModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_set"
    )

    objects = TenantManager()  # To zapewnia przezroczystość

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.user_id:
            current_user = get_current_user()
            if current_user:
                self.user = current_user

        super().save(*args, **kwargs)
