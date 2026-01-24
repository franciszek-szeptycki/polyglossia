from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from vocabulary.infrastructure.forms.word import WordForm
from vocabulary.infrastructure.models.word import Word


class WordListView(ListView):
    model = Word
    template_name = "words/list.html"
    context_object_name = "words"


class WordDetailView(DetailView):
    model = Word
    template_name = "words/detail.html"
    context_object_name = "word"


class WordCreateView(CreateView):
    model = Word
    form_class = WordForm
    template_name = "words/form.html"
    success_url = reverse_lazy("word_list")


class WordUpdateView(UpdateView):
    model = Word
    form_class = WordForm
    template_name = "words/form.html"
    success_url = reverse_lazy("word_list")


class WordDeleteView(DeleteView):
    model = Word
    template_name = "words/confirm_delete.html"
    success_url = reverse_lazy("word_list")
