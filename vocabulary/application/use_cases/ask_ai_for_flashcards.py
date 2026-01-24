from vocabulary.application.services.generate_flashcards import (
    ask_ai_for_flashcards_service,
)
from vocabulary.infrastructure.repositories.flashcard import flashcard_repository
from vocabulary.infrastructure.repositories.word import word_repository


class AskAIForFlashcardsUseCase:
    def execute(self, *, word_id: str):
        word = word_repository.get(word_id)

        flashcards = ask_ai_for_flashcards_service.execute(word=word)

        flashcard_repository.bulk_create(dtos=flashcards)


generate_flashcards_use_case = AskAIForFlashcardsUseCase()
