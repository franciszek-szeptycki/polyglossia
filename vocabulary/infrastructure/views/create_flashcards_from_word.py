from django.shortcuts import redirect
from django.views import View

from vocabulary.infrastructure.factories.container import container


class WordGenerateFlashcardsView(View):
    def dispatch(self, request, pk, *args, **kwargs):

        container.use_case_generate_flashcards_for_word.execute(word_id=pk)

        return redirect(request.META.get("HTTP_REFERER", "/"))
