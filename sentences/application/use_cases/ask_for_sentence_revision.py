from uuid import UUID

from sentences.application.dtos.sentece import SentenceDTO
from sentences.application.services.sentence_revision import (
    get_sentence_revision_service,
)
from sentences.infrastructure.repository.sentence import sentence_repository
from sentences.infrastructure.repository.sentence_revision import (
    sentence_revision_repository,
)


class AskForSentenceRevisionUseCase:
    def execute(self, *, sentence_dto: SentenceDTO) -> str:
        sentence_repository.create(sentence_dto=sentence_dto)

        sentence_revision_dto = get_sentence_revision_service.execute(
            sentence_dto=sentence_dto
        )

        sentence_revision_repository.create_from_dto(sentence_revision_dto)

        return sentence_revision_dto.id


ask_for_sentence_revision_use_case = AskForSentenceRevisionUseCase()
