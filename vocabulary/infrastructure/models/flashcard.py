from django.db import models

from vocabulary.infrastructure.models.word import Word


class Flashcard(models.Model):
    word = models.ForeignKey(
        Word, on_delete=models.SET_NULL, null=True, related_name="flashcards"
    )
    front = models.TextField()
    back = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    exported_at = models.DateTimeField(null=True, blank=True)

    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.SET_NULL, null=True, related_name="flashcards"
    )

    class Meta:
        ordering = [
            models.F("exported_at").desc(nulls_first=True),
            models.F("created_at").desc(),
        ]
