from vocabulary.application.dtos.word import WordDTO
from vocabulary.infrastructure.models.word import Word as WordModel


class WordRepository:
    def create(self, dto: WordDTO) -> WordDTO:
        word = WordModel.objects.create(id=dto.id, text=dto.text, context=dto.context)
        return WordDTO(id=str(word.id), text=word.text, context=word.context)

    def get(self, id: str) -> WordDTO:
        word = WordModel.objects.get(id=id)
        return WordDTO(id=str(word.id), text=word.text, context=word.context)


word_repository = WordRepository()
