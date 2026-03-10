from abc import ABC, abstractmethod
from typing import List

from vocabulary.application.dtos.word import WordDTO


class WordRepositoryABC(ABC):
    @abstractmethod
    def create(self, dto: WordDTO) -> WordDTO:
        pass

    @abstractmethod
    def get(self, id: str) -> WordDTO:
        pass

    @abstractmethod
    def generating_flash_cards_in_progress(self, *, word_id: str):
        pass

    @abstractmethod
    def generating_flash_cards_done(self, *, word_id: str):
        pass

    @abstractmethod
    def generating_flash_cards_failed(self, *, word_id: str):
        pass

    @abstractmethod
    def list(self) -> List[WordDTO]:
        pass
