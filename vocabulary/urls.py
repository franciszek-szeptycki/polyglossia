from django.urls import path

from vocabulary.infrastructure.views.create_flashcards_from_word import (
    WordGenerateFlashcardsView,
)
from vocabulary.infrastructure.views.flashcard_bulk_export import (
    FlashcardBulkExportView,
)
from vocabulary.infrastructure.views.flashcard_htmx_update import (
    FlashcardHtmxUpdateView,
)
from vocabulary.infrastructure.views.flashcard_list import FlashcardListView
from vocabulary.infrastructure.views.word_bulk_create import (
    WordBulkConfirmView,
    WordBulkCreateView,
)
from vocabulary.infrastructure.views.word_crud import (
    WordCreateView,
    WordDeleteView,
    WordDetailView,
    WordListView,
    WordUpdateView,
)
from vocabulary.infrastructure.views.word_next_redirect import WordNextRedirectView

urlpatterns = [
    path("", WordListView.as_view(), name="word_list"),
    path("add/", WordCreateView.as_view(), name="word_create"),
    path("<uuid:pk>/", WordDetailView.as_view(), name="word_detail"),
    path("<uuid:pk>/edit/", WordUpdateView.as_view(), name="word_edit"),
    path("<uuid:pk>/delete/", WordDeleteView.as_view(), name="word_delete"),
    path("add-bulk/", WordBulkCreateView.as_view(), name="word_bulk_create"),
    path("add-bulk/confirm/", WordBulkConfirmView.as_view(), name="word_bulk_confirm"),
    path(
        "next-word-redirect/",
        WordNextRedirectView.as_view(),
        name="word_next_redirect",
    ),
    path(
        "<uuid:pk>/generate-flashcards/",
        WordGenerateFlashcardsView.as_view(),
        name="word_generate_flashcards",
    ),
    path(
        "flashcards/<uuid:pk>/update-htmx/",
        FlashcardHtmxUpdateView.as_view(),
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
