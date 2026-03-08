from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.ports.word_repository import WordRepositoryABC
from vocabulary.application.services.create_eva_flashcards_service import (
    CreateEvaFlaschardsService,
)
from vocabulary.infrastructure.repositories.word_repository import word_repository


class GenerateFlashcardsForWordUseCase:
    def __init__(self, *, word_repo: WordRepositoryABC, llm_adapter: LLMAdapter):

        self.word_repo = word_repo

        self.llm_manager = CreateEvaFlaschardsService(llm_adapter=llm_adapter)

    def execute(self, *, word_id: str):

        word_dto = self.word_repo.get(word_id)

        # WORD as IN_PROGRESS
        self.word_repo.generating_flash_cards_in_progress(word_id=word_dto.id)

        try:
            # sentences = self.llm_manager.create_sentences(word=word_dto.text)

            # filtered_sentences = self.llm_manager.filter_sentences(
            #     sentences=sentences, word=word_dto.text
            # )

            # print(len(sentences))
            # print(len(filtered_sentences))

            # print(filtered_sentences)

            # WORD as DONE
            self.word_repo.generating_flash_cards_done(word_id=word_dto.id)

        except Exception as e:
            # WORD as FAILED
            self.word_repo.generating_flash_cards_failed(word_id=word_dto.id)
            print(f"Błąd podczas generowania fiszek: {e}")
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase(
    word_repo=word_repository,
    llm_adapter=ollama_adapter,
    # llm_adapter=openai_adapter
)
