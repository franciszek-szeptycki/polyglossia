from typing import Optional

from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.infrastructure.models.word import Word


class WordQuery:
    @staticmethod
    def list():
        return Word.objects.filter(profile=get_profile_id())

    @staticmethod
    def get_next_word_without_flashcards() -> Optional[Word]:
        words = Word.objects.filter(profile=get_profile_id()).order_by("created_at")
        return next((w for w in words if not w.has_active_flashcards()), None)
