from django.shortcuts import redirect
from django.views.generic import View

from vocabulary.infrastructure.models.word import Word


class WordNextRedirectView(View):
    def get(self, request, *args, **kwargs):
        words = Word.objects.all().order_by("created_at")  # i know, i know...
        next_word = next((w for w in words if not w.has_active_flashcards), None)

        if next_word:
            return redirect("word_detail", pk=next_word.id)
        else:
            return redirect("word_list")
