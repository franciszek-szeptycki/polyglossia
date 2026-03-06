from datetime import datetime
from typing import List

from common.repositories.user_context_repository import UserContextRepository
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.infrastructure.models.flashcard import Flashcard


class FlashcardRepository(UserContextRepository):
    def create(self, *, dto: FlashcardDTO):
        Flashcard.objects.create(
            user_id=self._get_user_id(),
            id=dto.id,
            word_id=dto.word_id,
            front=dto.front,
            back=dto.back,
        )

    def bulk_create(self, *, dtos: List[FlashcardDTO]):
        Flashcard.objects.bulk_create(
            [
                Flashcard(
                    id=dto.id,
                    word_id=dto.word_id,
                    front=dto.front,
                    back=dto.back,
                    user_id=self._get_user_id(),
                )
                for dto in dtos
            ]
        )

    def get_by_ids(self, ids: List[str]) -> List[FlashcardDTO]:
        queryset = Flashcard.objects.filter(
            id__in=ids,
            user_id=self._get_user_id(),
        )

        if queryset.count() != len(ids):
            raise ValueError("Some flashcards not found")

        return [
            FlashcardDTO(
                id=flashcard.id,
                word_id=flashcard.word_id,
                front=flashcard.front,
                back=flashcard.back,
                is_active=flashcard.is_active,
                exported_at=flashcard.exported_at,
                user_id=self._get_user_id(),
            )
            for flashcard in queryset
        ]

    def update_exported_at(self, *, ids: List[str], time: datetime):
        Flashcard.objects.filter(
            id__in=ids,
            user_id=self._get_user_id(),
        ).update(exported_at=time)


flashcard_repository = FlashcardRepository()
