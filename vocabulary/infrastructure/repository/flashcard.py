from typing import List

from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.infrastructure.models.flashcard import Flashcard as FlashcardModel


class FlashcardRepository:
    def create(self, *, dto: FlashcardDTO):
        FlashcardModel.objects.create(
            id=dto.id, word_id=dto.word_id, front=dto.front, back=dto.back
        )

    def bulk_create(self, *, dtos: List[FlashcardDTO]):
        FlashcardModel.objects.bulk_create(
            [
                FlashcardModel(
                    id=dto.id, word_id=dto.word_id, front=dto.front, back=dto.back
                )
                for dto in dtos
            ]
        )


flashcard_repository = FlashcardRepository()
