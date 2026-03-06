from django.shortcuts import redirect
from django.views import View

from vocabulary.application.use_cases.create_flashcards_from_word import (
    generate_flashcards_for_word_use_case,
)


class WordGenerateFlashcardsView(View):
    def dispatch(self, request, pk, *args, **kwargs):
        generate_flashcards_for_word_use_case.execute(word_id=pk)

        return redirect(request.META.get("HTTP_REFERER", "/"))
