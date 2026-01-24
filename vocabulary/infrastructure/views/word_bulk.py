from django import forms
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from vocabulary.infrastructure.forms.word_bulk_import import BulkImportForm
from vocabulary.infrastructure.models.word import Word


class WordBulkCreateView(FormView):
    template_name = "words/bulk_form.html"
    form_class = BulkImportForm

    def get_initial(self):
        initial = super().get_initial()
        bulk_data = self.request.session.get("bulk_data")

        if bulk_data:
            lines = [f"{item['text']}; {item['context']}" for item in bulk_data]
            initial["data"] = "\n".join(lines)

        return initial

    def form_valid(self, form):
        self.request.session["bulk_data"] = form.get_parsed_data()
        return redirect("word_bulk_confirm")


class WordBulkConfirmView(TemplateView):
    template_name = "words/bulk_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["preview_data"] = self.request.session.get("bulk_data", [])
        return context

    def post(self, request, *args, **kwargs):
        data = request.session.get("bulk_data", [])
        words_to_create = [
            Word(text=item["text"], context=item["context"]) for item in data
        ]
        Word.objects.bulk_create(words_to_create)
        del request.session["bulk_data"]
        return redirect("word_list")
