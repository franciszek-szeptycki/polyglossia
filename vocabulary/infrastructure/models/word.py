import uuid

from django.db import models

from multitenancy.models import TenantModel


class Word(TenantModel):
    class GeneratingAnkiStatus(models.TextChoices):
        NULL = "NULL", "NULL"
        IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
        FAILED = "FAILED", "FAILED"
        DONE = "DONE", "DONE"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255)
    context = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    generating_flashcards_status = models.CharField(
        max_length=20,
        choices=GeneratingAnkiStatus.choices,
        default=GeneratingAnkiStatus.NULL,
    )

    class Meta(TenantModel.Meta):
        ordering = ["-created_at"]

    @property
    def has_active_flashcards(self):
        return self.flashcards.filter(is_active=True).exists()

    @property
    def flashcards_number(self):
        return self.flashcards.count()
