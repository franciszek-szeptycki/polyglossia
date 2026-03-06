from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.services.create_raw_sentences import (
    CreateRawSentencesService,
)
from vocabulary.application.services.replace_word_in_sentence import (
    ReplaceWordInSentence,
)
from vocabulary.infrastructure.repositories.flashcard import flashcard_repository
from vocabulary.infrastructure.repositories.word import word_repository


class GenerateFlashcardsForWordUseCase:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.create_raw_sentences = CreateRawSentencesService(llm_adapter=llm_adapter)
        self.replace_word_in_sentence = ReplaceWordInSentence()

    def execute(self, *, word_id: str):
        word = word_repository.get(word_id)

        # WORD as IN_PROGRESS
        word_repository.generating_flash_cards_in_progress(word_id=word_id)

        try:
            sentences = self.create_raw_sentences.execute(word=word.text)

            sentences_with_blank = []
            for sentence in sentences:
                sentence_with_blank = self.replace_word_in_sentence.execute(
                    sentence=sentence, word=word.text
                )
                sentences_with_blank.append(sentence_with_blank)

            print(sentences_with_blank)

            # WORD as DONE
            word_repository.generating_flash_cards_done(word_id=word_id)

        except Exception as e:
            # WORD as FAILED
            word_repository.generating_flash_cards_failed(word_id=word_id)
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase(
    llm_adapter=ollama_adapter
    # llm_adapter=openai_adapter
)
