from concurrent.futures import ThreadPoolExecutor

from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.ports.word_repository import WordRepositoryABC
from vocabulary.application.services.create_raw_sentences import (
    CreateRawSentencesService,
)
from vocabulary.application.services.replace_word_in_sentence import (
    ReplaceWordInSentence,
)
from vocabulary.infrastructure.repositories.word_repository import word_repository


class GenerateFlashcardsForWordUseCase:
    def __init__(self, *, word_repo: WordRepositoryABC, llm_adapter: LLMAdapter):

        self.word_repo = word_repo

        self.create_raw_sentences = CreateRawSentencesService(llm_adapter=llm_adapter)
        self.replace_word_in_sentence = ReplaceWordInSentence()

    def execute(self, *, word_id: str):
        word = self.word_repo.get(word_id)

        # WORD as IN_PROGRESS
        self.word_repo.generating_flash_cards_in_progress(word_id=word_id)

        try:
            sentences = self.create_raw_sentences.execute(word=word.text)

            sentences_with_blank = []

            with ThreadPoolExecutor(max_workers=len(sentences)) as executor:
                results = executor.map(
                    lambda s: self.replace_word_in_sentence.execute(
                        sentence=s, word=word.text
                    ),
                    sentences,
                )

                sentences_with_blank = list(results)

            print(sentences_with_blank)

            # WORD as DONE
            self.word_repo.generating_flash_cards_done(word_id=word_id)

            return sentences_with_blank

        except Exception as e:
            # WORD as FAILED
            self.word_repo.generating_flash_cards_failed(word_id=word_id)
            print(f"Błąd podczas generowania fiszek: {e}")
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase(
    word_repo=word_repository,
    llm_adapter=ollama_adapter,
    # llm_adapter=openai_adapter
)
