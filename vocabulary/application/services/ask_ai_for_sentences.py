import json
import os
import pathlib
from typing import List
from uuid import uuid4

from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.application.dtos.raw_flashcard_data import RawFlashcardDataDTO
from vocabulary.application.dtos.word import WordDTO


class AskAiForSentencesService:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter: LLMAdapter = llm_adapter

        with open(
            os.path.join(
                pathlib.Path(__file__).resolve().parent,
                "prompts",
                "ask_ai_for_sentences.txt",
            )
        ) as file:
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


# if __name__ == "__main__":
#     ask_ai_for_sentences_service = AskAiForSentencesService()
#     word = WordDTO(id="", text="Haus", context="impreza")
#     raw_flashcards_data = ask_ai_for_sentences_service.execute(word=word)
#     for value in raw_flashcards_data:
#         print(value)
