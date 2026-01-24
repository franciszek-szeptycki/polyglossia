from typing import List

from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.infrastructure.models.flashcard import Flashcard


class FlashcardRepository:
    def create(self, *, dto: FlashcardDTO):
        Flashcard.objects.create(
            id=dto.id, word_id=dto.word_id, front=dto.front, back=dto.back
        )

    def bulk_create(self, *, dtos: List[FlashcardDTO]):
        Flashcard.objects.bulk_create(
            [
                Flashcard(
                    id=dto.id, word_id=dto.word_id, front=dto.front, back=dto.back
                )
                for dto in dtos
            ]
        )


flashcard_repository = FlashcardRepository()
