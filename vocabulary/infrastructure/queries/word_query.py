from typing import Optional

from django.db.models import Count, Exists, OuterRef

from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.infrastructure.models.flashcard import Flashcard
from vocabulary.infrastructure.models.word import Word


class WordQuery:
    @staticmethod
    def list():
        active_flashcards_exists = Flashcard.objects.filter(
            word=OuterRef("pk"), is_active=True
        )

        return Word.objects.filter(profile=get_profile_id()).annotate(
            annotated_has_active_flashcards=Exists(active_flashcards_exists),
            flashcards_count=Count("flashcards"),
        )

    @staticmethod
    def get_next_word_without_flashcards() -> Optional[Word]:
        words = Word.objects.filter(profile=get_profile_id()).order_by("created_at")
        return next((w for w in words if not w.has_active_flashcards), None)
