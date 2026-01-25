from django.views.generic import ListView

from vocabulary.infrastructure.models import Flashcard


class FlashcardListView(ListView):
    model = Flashcard
    template_name = "flashcards/list.html"
    context_object_name = "flashcards"

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_count"] = self.get_queryset().count()
        return context
