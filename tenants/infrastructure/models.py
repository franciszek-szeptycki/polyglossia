from django.db import models

from tenants.consts import Language


class Tenant(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name="tenant")
    language = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in Language],
        default=Language.GERMAN.value
    )
