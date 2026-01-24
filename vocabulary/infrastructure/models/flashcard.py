from django.db import models

from vocabulary.infrastructure.models.word import Word


class Flashcard(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="flashcards")
    front = models.TextField()
    back = models.TextField()
