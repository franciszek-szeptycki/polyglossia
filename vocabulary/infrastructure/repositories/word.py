from vocabulary.application.dtos.word import WordDTO
from vocabulary.infrastructure.models.word import Word as WordModel


class WordRepository:
    def create(self, dto: WordDTO) -> WordDTO:
        word = WordModel.objects.create(id=dto.id, text=dto.text, context=dto.context)
        return WordDTO(id=str(word.id), text=word.text, context=word.context)

    def get(self, id: str) -> WordDTO:
        word = WordModel.objects.get(id=id)
        return WordDTO(id=str(word.id), text=word.text, context=word.context)

    def generating_flash_cards_in_progress(self, *, word_id: str):
        WordModel.objects.filter(id=word_id).update(
            generating_anki_status=WordModel.GeneratingAnkiStatus.IN_PROGRESS
        )

    def generating_flash_cards_done(self, *, word_id: str):
        WordModel.objects.filter(id=word_id).update(
            generating_anki_status=WordModel.GeneratingAnkiStatus.DONE
        )

    def generating_flash_cards_failed(self, *, word_id: str):
        WordModel.objects.filter(id=word_id).update(
            generating_anki_status=WordModel.GeneratingAnkiStatus.FAILED
        )


word_repository = WordRepository()
