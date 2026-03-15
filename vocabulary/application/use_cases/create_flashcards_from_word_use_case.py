from common.adapters.ollama_adapter import ollama_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.domain.ports.flashcard_repository import FlashcardRepositoryABC
from vocabulary.domain.ports.word_repository import WordRepositoryABC
from vocabulary.domain.services.create_flashcards_service import (
    CreateFlaschardsService,
)
from vocabulary.infrastructure.adapters.prompt_manager import (
    PromptManagersContainer,
)
from profiles.domain.entities import ProfileDTO


class GenerateFlashcardsForWordUseCase:
    def __init__(
        self,
        *,
        word_repo: WordRepositoryABC,
        flashcard_repo: FlashcardRepositoryABC,
        llm_adapter: LLMAdapter,
    ):
        self.word_repo = word_repo
        self.flashcard_repo = flashcard_repo

        prompt_mng_container = PromptManagersContainer(llm_adapter=llm_adapter)
        self.create_flashcard_svc = CreateFlaschardsService(
            prompt_managers=prompt_mng_container
        )

    def execute(self, *, word_id: str, profile: ProfileDTO):

        word_dto = self.word_repo.get(word_id)

        # WORD as IN_PROGRESS
        self.word_repo.generating_flash_cards_in_progress(word_id=word_dto.id)

        try:
            flashcards = self.create_flashcard_svc.execute(
                word=word_dto.text,
                language=profile.language
            )
            for card in flashcards:
                flashcard = FlashcardDTO(
                    word_id=word_dto.id,
                    front=card.front,
                    back=card.back,
                )
                self.flashcard_repo.create(dto=flashcard)

            # WORD as DONE
            self.word_repo.generating_flash_cards_done(word_id=word_dto.id)

        except Exception as e:
            # WORD as FAILED
            self.word_repo.generating_flash_cards_failed(word_id=word_dto.id)
            print(f"Błąd podczas generowania fiszek: {e}")
            raise e
