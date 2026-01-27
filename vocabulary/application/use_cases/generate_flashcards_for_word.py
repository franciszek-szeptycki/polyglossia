from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.services.ask_ai_for_sentences import (
    AskAiForSentencesService,
)
from vocabulary.application.services.generate_flashcards import (
    GenerateFlashcardsService,
)
from vocabulary.infrastructure.repositories.flashcard import flashcard_repository
from vocabulary.infrastructure.repositories.word import word_repository


class GenerateFlashcardsForWordUseCase:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.ask_ai_for_sentences: AskAiForSentencesService = AskAiForSentencesService(
            llm_adapter=llm_adapter
        )
        self.generate_flashcards: GenerateFlashcardsService = GenerateFlashcardsService(
            llm_adapter=llm_adapter
        )

    def execute(self, *, word_id: str):
        word = word_repository.get(word_id)

        word_repository.generating_flash_cards_in_progress(word_id=word_id)

        try:
            raw_flashcards_data = self.ask_ai_for_sentences.execute(word=word)
            flashcards = self.generate_flashcards.execute(
                raw_flashcards_data=raw_flashcards_data, word_id=word.id
            )

            flashcard_repository.bulk_create(dtos=flashcards)

            word_repository.generating_flash_cards_done(word_id=word_id)

        except Exception as e:
            word_repository.generating_flash_cards_failed(word_id=word_id)
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase(
    llm_adapter=ollama_adapter
    # llm_adapter=openai_adapter
)
