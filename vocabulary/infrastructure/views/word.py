from django.urls import reverse, reverse_lazy
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

    def get_queryset(self):
        queryset = super().get_queryset()
        self.active_filter = self.request.GET.get("active_flashcards")
        if self.active_filter == "yes":
            queryset = queryset.filter(flashcards__is_selected=True).distinct()
        elif self.active_filter == "no":
            queryset = queryset.exclude(flashcards__is_selected=True).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_count"] = self.get_queryset().count()
        context["current_filter"] = self.active_filter
        return context


class WordDetailView(DetailView):
    model = Word
    template_name = "words/detail.html"
    context_object_name = "word"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flashcards"] = self.object.flashcards.all()
        return context


class WordCreateView(CreateView):
    model = Word
    form_class = WordForm
    template_name = "generic/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "słowo"
        context["cancel_url"] = reverse("word_list")
        return context

    def get_success_url(self):
        # self.object to nowo utworzony obiekt Word
        return reverse("word_detail", kwargs={"pk": self.object.pk})


class WordUpdateView(UpdateView):
    model = Word
    form_class = WordForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("word_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "słowo"
        context["cancel_url"] = reverse_lazy("word_list")
        return context


class WordDeleteView(DeleteView):
    model = Word
    template_name = "words/confirm_delete.html"
    success_url = reverse_lazy("word_list")
