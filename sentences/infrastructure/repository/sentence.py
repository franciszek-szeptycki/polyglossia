from sentences.application.dtos.sentence import SentenceDTO
from sentences.infrastructure.models.sentence import Sentence


class SentenceRepository:
    def create(self, *, sentence_dto: SentenceDTO):
        return Sentence.objects.create(original_text=sentence_dto.original_text)


sentence_repository = SentenceRepository()
