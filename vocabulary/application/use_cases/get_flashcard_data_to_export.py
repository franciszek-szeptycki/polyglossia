from datetime import datetime
from typing import List

from vocabulary.infrastructure.repositories.flashcard import (
    flashcard_repository,
)


class GetFlashcardDataToExportUseCase:
    def execute(self, *, card_ids: List[str], time: datetime) -> List[List[str]]:
        flashcards = flashcard_repository.get_by_ids(card_ids)

        lines = []
        for card in flashcards:
            lines.append([card.front, card.back])

        flashcard_repository.update_exported_at(
            ids=[card.id for card in flashcards], time=time
        )

        return lines


get_flashcard_data_to_export_use_case = GetFlashcardDataToExportUseCase()
