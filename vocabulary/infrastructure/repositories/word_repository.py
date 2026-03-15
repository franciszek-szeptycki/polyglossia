from typing import List

from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.application.dtos.word import WordDTO
from vocabulary.domain.ports.word_repository import WordRepositoryABC
from vocabulary.infrastructure.models.word import Word as WordModel


class WordRepository(WordRepositoryABC):
    def create(self, dto: WordDTO) -> WordDTO:
        word = WordModel.objects.create(
            id=dto.id,
            text=dto.text,
            context=dto.context,
            profile=get_profile_id(),
        )
        return self._to_dto(word)

    def get(self, id: str) -> WordDTO:
        word = WordModel.objects.get(
            id=id,
            profile=get_profile_id(),
        )
        return self._to_dto(word)

    def _update_status(self, word_id: str, status: WordModel.GeneratingAnkiStatus):
        updated_count = WordModel.objects.filter(
            id=word_id,
            profile=get_profile_id(),
        ).update(generating_flashcards_status=status)

        if updated_count == 0:
            raise ValueError(
                f"Słowo o ID {word_id} nie istnieje lub nie masz do niego uprawnień."
            )

    def generating_flash_cards_in_progress(self, *, word_id: str):
        self._update_status(word_id, WordModel.GeneratingAnkiStatus.IN_PROGRESS)

    def generating_flash_cards_done(self, *, word_id: str):
        self._update_status(word_id, WordModel.GeneratingAnkiStatus.DONE)

    def generating_flash_cards_failed(self, *, word_id: str):
        self._update_status(word_id, WordModel.GeneratingAnkiStatus.FAILED)

    def _to_dto(self, word: WordModel) -> WordDTO:
        return WordDTO(
            id=str(word.id),
            text=str(word.text),
            context=str(word.context),
            profile_id=int(word.profile.id),
        )

    def list(self) -> List[WordDTO]:
        words = WordModel.objects.filter(
            profile=get_profile_id(),
        )
        return [self._to_dto(word) for word in words]


word_repository = WordRepository()
