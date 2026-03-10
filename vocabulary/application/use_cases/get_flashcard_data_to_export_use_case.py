from datetime import datetime
from typing import List

from vocabulary.domain.ports.flashcard_repository import FlashcardRepositoryABC


class GetFlashcardDataToExportUseCase:
    def __init__(self, *, flashcard_repo: FlashcardRepositoryABC):
        self._flashcard_repo = flashcard_repo

    def execute(self, *, card_ids: List[str], time: datetime) -> List[List[str]]:
        flashcards = self._flashcard_repo.get_by_ids(card_ids)

        lines = []
        for card in flashcards:
            lines.append([card.front, card.back])

        self._flashcard_repo.update_exported_at(
            ids=[card.id for card in flashcards], time=time
        )

        return lines
