from datetime import datetime
from typing import List

from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.domain.ports.flashcard_repository import FlashcardRepositoryABC
from vocabulary.infrastructure.models.flashcard import Flashcard


class FlashcardRepository(FlashcardRepositoryABC):
    def create(self, *, dto: FlashcardDTO):
        Flashcard.objects.create(
            profile_id=get_profile_id(),
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
                    profile_id=get_profile_id(),
                )
                for dto in dtos
            ]
        )

    def get_by_ids(self, ids: List[str]) -> List[FlashcardDTO]:
        queryset = Flashcard.objects.filter(
            id__in=ids,
            profile_id=get_profile_id(),
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
                profile_id=get_profile_id(),
            )
            for flashcard in queryset
        ]

    def update_exported_at(self, *, ids: List[str], time: datetime):
        Flashcard.objects.filter(
            id__in=ids,
            profile_id=get_profile_id(),
        ).update(exported_at=time)
