from common.ports.llm_adapter import LLMAdapter
from profiles.domain.entities import ProfileDTO
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.application.ports.flashcard_repository import FlashcardRepositoryABC
from vocabulary.application.ports.word_repository import WordRepositoryABC
from vocabulary.application.services.create_flashcards_service import (
    CreateFlaschardsService,
)
from vocabulary.application.services.german import GermanFlashcardsService
from vocabulary.application.services.spanish import SpanishFlashcardsService
from vocabulary.infrastructure.adapters.prompt_manager import (
    PromptManagersContainer,
)


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
        self.spanish_flashcards = SpanishFlashcardsService(llm=llm_adapter)
        self.german_flashcards = GermanFlashcardsService(llm=llm_adapter)

    def execute(self, *, word_id: str, profile: ProfileDTO):

        word = self.word_repo.get(word_id)

        # WORD as IN_PROGRESS
        self.word_repo.generating_flash_cards_in_progress(word_id=word.id)

        try:
            if profile.language == "spanish":
                flashcards = self.spanish_flashcards.execute(word=word.text)
            elif profile.language == "german":
                flashcards = self.german_flashcards.execute(word=word.text)
            else:
                flashcards = self.create_flashcard_svc.execute(
                    word=word.text,
                    language=profile.language,
                    context=word.context,
                )
            for card in flashcards:
                flashcard = FlashcardDTO(
                    word_id=word.id,
                    front=card.front,
                    back=card.back,
                )
                self.flashcard_repo.create(dto=flashcard)

            # WORD as DONE
            self.word_repo.generating_flash_cards_done(word_id=word.id)

        except Exception as e:
            # WORD as FAILED
            self.word_repo.generating_flash_cards_failed(word_id=word.id)
            print(f"Błąd podczas generowania fiszek: {e}")
            raise e
