from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from vocabulary.infrastructure.models import Flashcard
from vocabulary.infrastructure.queries.flashcard_query import FlashcardQuery


class FlashcardListView(LoginRequiredMixin, ListView):
    model = Flashcard
    template_name = "flashcards/list.html"
    context_object_name = "flashcards"

    def get_queryset(self):
        return FlashcardQuery.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_count"] = self.get_queryset().count()
        return context
