from vocabulary.application.services.ask_ai_for_sentences import (
    ask_ai_for_sentences_service,
)
from vocabulary.application.services.generate_flashcards import (
    generate_flashcards_service,
)
from vocabulary.infrastructure.repositories.flashcard import flashcard_repository
from vocabulary.infrastructure.repositories.word import word_repository


class GenerateFlashcardsForWordUseCase:
    def execute(self, *, word_id: str):
        word = word_repository.get(word_id)

        word_repository.generating_flash_cards_in_progress(word_id=word_id)

        try:
            raw_flashcards_data = ask_ai_for_sentences_service.execute(word=word)
            flashcards = generate_flashcards_service.execute(
                raw_flashcards_data=raw_flashcards_data, word_id=word.id
            )

            flashcard_repository.bulk_create(dtos=flashcards)

            word_repository.generating_flash_cards_done(word_id=word_id)

        except Exception as e:
            word_repository.generating_flash_cards_failed(word_id=word_id)
            raise e


generate_flashcards_for_word_use_case = GenerateFlashcardsForWordUseCase()
