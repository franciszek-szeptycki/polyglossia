from django.views.generic import DetailView, ListView

from sentences.infrastructure.models.sentence_revision import SentenceRevision


class SentenceRevisionDetailView(DetailView):
    model = SentenceRevision
    template_name = "sentence_revisions/detail.html"
    context_object_name = "revision_item"


class SentenceRevisionListView(ListView):
    model = SentenceRevision
    template_name = "sentence_revisions/list.html"
    context_object_name = "revisions"
    ordering = ["-created_at"]
