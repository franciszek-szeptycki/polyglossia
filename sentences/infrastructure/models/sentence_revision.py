from django.db import models


class SentenceRevision(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=True,
    )
    original_text = models.TextField(default="")
    translated_text = models.TextField(default="")
    revision = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
