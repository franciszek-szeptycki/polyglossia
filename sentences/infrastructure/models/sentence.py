from django.db import models


class Sentence(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
