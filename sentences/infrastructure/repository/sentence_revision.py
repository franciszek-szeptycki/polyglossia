from sentences.application.dtos.sentence_revision import SentenceRevisionDTO
from sentences.infrastructure.models.sentence_revision import SentenceRevision


class SentenceRevisionRepository:
    def create_from_dto(self, dto: SentenceRevisionDTO) -> SentenceRevisionDTO:
        obj = SentenceRevision.objects.create(
            id=dto.id, text=dto.text, revision=dto.revision
        )
        return SentenceRevisionDTO(id=str(obj.id), text=obj.text, revision=obj.revision)


sentence_revision_repository = SentenceRevisionRepository()
