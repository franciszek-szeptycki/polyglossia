from django.shortcuts import redirect
from django.views import View

from vocabulary.application.use_cases.ask_ai_for_flashcards import (
    generate_flashcards_use_case,
)


class WordGenerateFlashcardsView(View):
    def dispatch(self, request, pk, *args, **kwargs):
        generate_flashcards_use_case.execute(word_id=pk)

        return redirect(request.META.get("HTTP_REFERER", "/"))
