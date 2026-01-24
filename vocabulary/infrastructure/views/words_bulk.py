from django import forms
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from vocabulary.infrastructure.models.word import Word


class BulkImportForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 15})
    )

    def get_parsed_data(self):
        lines = self.cleaned_data["data"].splitlines()
        parsed = []
        for line in lines:
            if ";" in line:
                text, context = line.split(";", 1)
                parsed.append({"text": text.strip(), "context": context.strip()})
        return parsed


class WordBulkCreateView(FormView):
    template_name = "words/bulk_form.html"
    form_class = BulkImportForm

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
