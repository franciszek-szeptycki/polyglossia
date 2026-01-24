from django.urls import path

from sentences.infrastructure.views.sentence import ContactView
from sentences.infrastructure.views.sentence_revision import (
    SentenceRevisionDetailView,
    SentenceRevisionListView,
)

urlpatterns = [
    path("", ContactView.as_view(), name="create_sentence"),
    path(
        "revisions/", SentenceRevisionListView.as_view(), name="sentence_revision_list"
    ),
    path(
        "revisions/<str:pk>/",
        SentenceRevisionDetailView.as_view(),
        name="sentence_revision_detail",
    ),
]
