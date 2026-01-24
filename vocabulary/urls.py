from django.urls import path

from vocabulary.infrastructure.views.flashcard import FlashcardListView
from vocabulary.infrastructure.views.flashcard_bulk_export import (
    FlashcardBulkExportView,
)
from vocabulary.infrastructure.views.flashcard_htmx import FlashcardUpdateHTMXView
from vocabulary.infrastructure.views.word import (
    WordCreateView,
    WordDeleteView,
    WordDetailView,
    WordListView,
    WordUpdateView,
)
from vocabulary.infrastructure.views.word_bulk import (
    WordBulkConfirmView,
    WordBulkCreateView,
)
from vocabulary.infrastructure.views.word_generate_flashcards import (
    WordGenerateFlashcardsView,
)

urlpatterns = [
    path("", WordListView.as_view(), name="word_list"),
    path("add/", WordCreateView.as_view(), name="word_create"),
    path("<uuid:pk>/", WordDetailView.as_view(), name="word_detail"),
    path("<uuid:pk>/edit/", WordUpdateView.as_view(), name="word_edit"),
    path("<uuid:pk>/delete/", WordDeleteView.as_view(), name="word_delete"),
    path("add-bulk/", WordBulkCreateView.as_view(), name="word_bulk_create"),
    path("add-bulk/confirm/", WordBulkConfirmView.as_view(), name="word_bulk_confirm"),
    path(
        "<uuid:pk>/generate-flashcards/",
        WordGenerateFlashcardsView.as_view(),
        name="word_generate_flashcards",
    ),
    path(
        "flashcards/<uuid:pk>/update-htmx/",
        FlashcardUpdateHTMXView.as_view(),
        name="flashcard_update_htmx",
    ),
    path(
        "flashcards/",
        FlashcardListView.as_view(),
        name="flashcard_list",
    ),
    path(
        "flashcards/bulk-export/",
        FlashcardBulkExportView.as_view(),
        name="flashcard_bulk_export",
    ),
]
