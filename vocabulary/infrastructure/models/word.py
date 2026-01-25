import uuid

from django.db import models


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255)
    context = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def has_active_flashcards(self):
        return self.flashcards.filter(is_active=True).exists()

    @property
    def flashcards_number(self):
        return self.flashcards.count()
