from sentences.application.dtos.sentece import SentenceDTO
from sentences.infrastructure.repository.sentence import sentence_repository


class AskForSentenceRevisionUseCase:
    def execute(self, *, sentence_dto: SentenceDTO):
        sentence_repository.create(sentence_dto=sentence_dto)


ask_for_sentence_revision_use_case = AskForSentenceRevisionUseCase()
