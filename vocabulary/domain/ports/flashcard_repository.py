from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from vocabulary.application.dtos.flashcard import FlashcardDTO


class FlashcardRepositoryABC(ABC):
    @abstractmethod
    def create(self, *, dto: FlashcardDTO) -> None:
        pass

    @abstractmethod
    def bulk_create(self, *, dtos: List[FlashcardDTO]) -> None:
        pass

    @abstractmethod
    def get_by_ids(self, ids: List[str]) -> List[FlashcardDTO]:
        pass

    @abstractmethod
    def update_exported_at(self, *, ids: List[str], time: datetime) -> None:
        pass
