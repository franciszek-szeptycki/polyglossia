import json
import os
import pathlib
from typing import List
from uuid import uuid4

from common.adapters.openai_adapter import openai_adapter
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.application.dtos.raw_flashcard_data import RawFlashcardDataDTO
from vocabulary.application.dtos.word import WordDTO


class AskAiForSentencesService:
    PROMPT_FILE_PATH = os.path.join(
        pathlib.Path(__file__).resolve().parent, "prompts", "ask_ai_for_sentences.txt"
    )

    def __init__(self):
        with open(self.PROMPT_FILE_PATH) as file:
            self.system_prompt = file.read()

    def execute(self, *, word: WordDTO) -> List[RawFlashcardDataDTO]:
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
            RawFlashcardDataDTO(
                word=word.text,
                target_language_sentence=item["target_language_sentence"],
                sentence_translation=item["sentence_translation"],
            )
            for item in json.loads(response)
        ]


ask_ai_for_sentences_service = AskAiForSentencesService()

if __name__ == "__main__":
    word = WordDTO(id="", text="Haus", context="impreza")
    flashcards_raw_data = ask_ai_for_sentences_service.execute(word=word)
    for value in flashcards_raw_data:
        print(value)
