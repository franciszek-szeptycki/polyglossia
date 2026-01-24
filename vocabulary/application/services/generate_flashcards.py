import json
import os
import pathlib
from typing import List
from uuid import uuid4

from common.adapters.openai_adapter import openai_adapter
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.application.dtos.word import WordDTO


class GenerateFlashcardsService:
    PROMPT_FILE_PATH = os.path.join(
        pathlib.Path(__file__).resolve().parent, "prompts", "generate_flashcards.txt"
    )

    def __init__(self):
        with open(self.PROMPT_FILE_PATH) as file:
            self.system_prompt = file.read()

    def execute(self, *, word: WordDTO) -> List[FlashcardDTO]:
        user_prompt = f"""
        słówko: {word.text}
        kontekst: {word.context}
        """

        response = openai_adapter.generate_response(
            system=self.system_prompt,
            user=user_prompt,
        )

        if not response:
            raise ValueError("No response received from OpenAI")

        return [
            FlashcardDTO(id=str(uuid4()), front=item["front"], back=item["back"])
            for item in json.loads(response)
        ]


generate_flashcards_service = GenerateFlashcardsService()

if __name__ == "__main__":
    word = WordDTO(id="", text="example", context="example context")
    flashcard = generate_flashcards_service.execute(word=word)
    print(flashcard)
