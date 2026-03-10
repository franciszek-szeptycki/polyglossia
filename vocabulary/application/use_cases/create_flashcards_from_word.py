from common.adapters.ollama_adapter import ollama_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.managers.prompt_manager import (
    PromptManagersContainer,
)
from vocabulary.application.ports.word_repository import WordRepositoryABC
from vocabulary.application.services.create_eva_flashcards_service import (
    CreateEvaFlaschardsService,
)
from vocabulary.infrastructure.repositories.word_repository import word_repository


class GenerateFlashcardsForWordUseCase:
    def __init__(self, *, word_repo: WordRepositoryABC, llm_adapter: LLMAdapter):

        self.word_repo = word_repo

        prompt_mng_container = PromptManagersContainer(llm_adapter=llm_adapter)

        self.create_eva_flashcard_svc_de = CreateEvaFlaschardsService(
            prompt_manager=prompt_mng_container.de_regular
        )

    def execute(self, *, word_id: str):

        word_dto = self.word_repo.get(word_id)

        # WORD as IN_PROGRESS
        self.word_repo.generating_flash_cards_in_progress(word_id=word_dto.id)

        try:
            self.create_eva_flashcard_svc_de

            self.word_repo.generating_flash_cards_done(word_id=word_dto.id)

        except Exception as e:
            # WORD as FAILED
            self.word_repo.generating_flash_cards_failed(word_id=word_dto.id)
            print(f"Błąd podczas generowania fiszek: {e}")
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase(
    word_repo=word_repository,
    llm_adapter=ollama_adapter,
)
