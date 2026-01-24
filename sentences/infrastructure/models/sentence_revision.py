from django.db import models


class SentenceRevision(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=True,
    )
    text = models.TextField()
    revision = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
