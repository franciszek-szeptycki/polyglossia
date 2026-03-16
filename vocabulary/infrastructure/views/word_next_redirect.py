from django.shortcuts import redirect
from django.views.generic import View

from vocabulary.infrastructure.models.word import Word
from vocabulary.infrastructure.queries.word_query import WordQuery


class WordNextRedirectView(View):
    def get(self, request, *args, **kwargs):
        next_word = WordQuery.get_next_word_without_flashcards()

        if next_word:
            return redirect("word_detail", pk=next_word.id)
        else:
            return redirect("word_list")
