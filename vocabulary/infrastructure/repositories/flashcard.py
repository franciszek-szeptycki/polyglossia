from datetime import datetime
from typing import List

from multitenancy.thread_local import get_current_user
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.infrastructure.models.flashcard import Flashcard


class FlashcardRepository:
    def create(self, *, dto: FlashcardDTO):
        user = get_current_user()
        Flashcard.objects.create(
            id=dto.id,
            word_id=dto.word_id,
            front=dto.front,
            back=dto.back,
            user=user,
        )

    def bulk_create(self, *, dtos: List[FlashcardDTO]):
        user = get_current_user()

        if not user:
            raise PermissionError("Cannot create flashcards without a tenant user.")

        Flashcard.objects.bulk_create(
            [
                Flashcard(
                    id=dto.id,
                    word_id=dto.word_id,
                    front=dto.front,
                    back=dto.back,
                    user=user,
                )
                for dto in dtos
            ]
        )

    def get_by_ids(self, ids: List[str]) -> List[FlashcardDTO]:
        queryset = Flashcard.objects.filter(id__in=ids)

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
            )
            for flashcard in queryset
        ]

    def update_exported_at(self, *, ids: List[str], time: datetime):
        Flashcard.objects.filter(id__in=ids).update(exported_at=time)


flashcard_repository = FlashcardRepository()
