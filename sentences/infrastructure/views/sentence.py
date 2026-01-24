from django.shortcuts import redirect, render
from django.views import View

from sentences.application.use_cases.ask_for_sentence_revision import (
    ask_for_sentence_revision_use_case,
)
from sentences.infrastructure.forms.sentence import SentenceForm
from sentences.infrastructure.repository.sentence import (
    SentenceRepository,
    sentence_repository,
)


class ContactView(View):
    template_name = "sentence.html"

    def get(self, request):
        form = SentenceForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence_dto = form.to_dto()

            ask_for_sentence_revision_use_case.execute(sentence_dto=sentence_dto)
            # return redirect("")

        return render(request, self.template_name, {"form": form})
