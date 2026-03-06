from django.views.generic import UpdateView

from vocabulary.infrastructure.models.flashcard import Flashcard


class FlashcardHtmxUpdateView(UpdateView):
    model = Flashcard
    fields = ["front", "back", "is_active"]
    template_name = "partials/flashcard_row.html"

    def form_valid(self, form):
        self.object = form.save()
        return self.render_to_response(self.get_context_data(card=self.object))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card"] = self.object
        return context
