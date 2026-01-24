from sentences.application.dtos.sentence_revision import SentenceRevisionDTO
from sentences.infrastructure.models.sentence_revision import SentenceRevision


class SentenceRevisionRepository:
    def create_from_dto(self, dto: SentenceRevisionDTO):
        SentenceRevision.objects.create(
            id=dto.id,
            original_text=dto.original_text,
            translated_text=dto.translated_text,
            revision=dto.revision,
        )


sentence_revision_repository = SentenceRevisionRepository()
