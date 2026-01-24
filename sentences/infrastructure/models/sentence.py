from django.db import models

from sentences.application.dtos.sentece import SentenceDTO


class Sentence(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
