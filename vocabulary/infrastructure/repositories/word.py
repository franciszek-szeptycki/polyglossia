from typing import List

from common.repositories.user_context_repository import UserContextRepository
from vocabulary.application.dtos.word import WordDTO
from vocabulary.infrastructure.models.word import Word as WordModel


class WordRepository(UserContextRepository):
    def create(self, dto: WordDTO) -> WordDTO:
        word = WordModel.objects.create(
            id=dto.id,
            text=dto.text,
            context=dto.context,
            user=self._get_user_id(),
        )
        return self._to_dto(word)

    def get(self, id: str) -> WordDTO:
        word = WordModel.objects.get(
            id=id,
            user=self._get_user_id(),
        )
        return self._to_dto(word)

    def _update_status(self, word_id: str, status: WordModel.GeneratingAnkiStatus):
        updated_count = WordModel.objects.filter(
            id=word_id,
            user=self._get_user_id(),
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
            user_id=word.user,
        )


word_repository = WordRepository()
