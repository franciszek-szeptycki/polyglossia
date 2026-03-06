from django.db import models


class Profile(models.Model):
    class Language(models.TextChoices):
        GERMAN = "GERMAN", "German"
        SPANISH = "SPANISH", "Spanish"

    user = models.OneToOneField(
        on_delete=models.CASCADE,
        to="auth.User",
    )

    language = models.CharField(
        max_length=100,
        choices=Language.choices,
    )
