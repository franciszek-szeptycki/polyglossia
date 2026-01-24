from sentences.application.dtos.sentece import SentenceDTO
from sentences.infrastructure.models.sentence import Sentence


class SentenceRepository:
    def create(self, *, sentence_dto: SentenceDTO):
        return Sentence.objects.create(text=sentence_dto.text)


sentence_repository = SentenceRepository()
