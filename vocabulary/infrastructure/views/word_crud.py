from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from vocabulary.infrastructure.factories.container import container
from vocabulary.infrastructure.forms.word_form import WordForm
from vocabulary.infrastructure.models.word import Word
from vocabulary.infrastructure.queries.word_query import WordQuery


class WordListView(LoginRequiredMixin, ListView):
    model = Word
    template_name = "words/list.html"
    context_object_name = "words"

    def get_queryset(self):
        queryset = WordQuery.list()

        self.active_filter = self.request.GET.get("active_flashcards")
        if self.active_filter == "yes":
            queryset = queryset.filter(flashcards__is_active=True).distinct()
        elif self.active_filter == "no":
            queryset = queryset.exclude(flashcards__is_active=True).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Używamy zafiltrowanego querysetu do licznika
        context["total_count"] = self.get_queryset().count()
        context["current_filter"] = self.active_filter
        return context


class WordDetailView(LoginRequiredMixin, DetailView):
    model = Word
    template_name = "words/detail.html"
    context_object_name = "word"

    def get_queryset(self):
        return WordQuery.list().prefetch_related("flashcards")


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    form_class = WordForm
    template_name = "generic/form.html"

    def form_valid(self, form):
        # Automatycznie przypisujemy zalogowanego użytkownika przed zapisem
        form.instance.profile_id = self.request.profile.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "słowo"
        context["cancel_url"] = reverse("word_list")
        return context

    def get_success_url(self):
        return reverse("word_detail", kwargs={"pk": self.object.pk})


class WordUpdateView(LoginRequiredMixin, UpdateView):
    model = Word
    form_class = WordForm
    template_name = "generic/form.html"
    success_url = reverse_lazy("word_list")

    def get_queryset(self):
        # User może edytować tylko swoje słówka
        return WordQuery.list()



class WordDeleteView(LoginRequiredMixin, DeleteView):
    model = Word
    template_name = "words/confirm_delete.html"
    success_url = reverse_lazy("word_list")

    def get_queryset(self):
        # User może usunąć tylko swoje słówka
        return WordQuery.list()
