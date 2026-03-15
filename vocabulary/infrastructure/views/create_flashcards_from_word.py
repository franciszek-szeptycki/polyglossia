import threading
from contextvars import copy_context
from django.shortcuts import redirect
from django.views import View

from vocabulary.infrastructure.factories.container import container


class WordGenerateFlashcardsView(View):
    def dispatch(self, request, pk, *args, **kwargs):
        ctx = copy_context()

        profile = request.profile

        def run_task():
            container.use_case_generate_flashcards_for_word.execute(word_id=pk, profile=profile)

        thread = threading.Thread(target=ctx.run, args=(run_task,))
        thread.start()

        return redirect(request.META.get("HTTP_REFERER", "/"))
