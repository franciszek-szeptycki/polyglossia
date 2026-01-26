from django.db import models

from multitenancy.models import TenantModel
from vocabulary.infrastructure.models.word import Word


class Flashcard(TenantModel):
    id = models.UUIDField(primary_key=True, editable=False)
    word = models.ForeignKey(
        Word, on_delete=models.SET_NULL, null=True, related_name="flashcards"
    )
    front = models.TextField()
    back = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    exported_at = models.DateTimeField(null=True, blank=True)

    class Meta(TenantModel.Meta):
        ordering = [
            models.F("exported_at").desc(nulls_first=True),
            models.F("created_at").desc(),
        ]
