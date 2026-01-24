from django.views.generic import ListView

from vocabulary.infrastructure.models import Flashcard


class FlashcardListView(ListView):
    model = Flashcard
    template_name = "flashcards/list.html"
    context_object_name = "flashcards"
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
