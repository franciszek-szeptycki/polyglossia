import json
import os
import pathlib
from typing import List
from uuid import uuid4

from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import FlashcardDTO
from vocabulary.application.dtos.raw_flashcard_data import RawFlashcardDataDTO


class GenerateFlashcardsService:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter: LLMAdapter = llm_adapter

        with open(
            os.path.join(
                pathlib.Path(__file__).resolve().parent,
                "prompts",
                "generate_flashcards.txt",
            )
        ) as file:
            self.system_prompt = file.read()

    def execute(
        self, *, raw_flashcards_data: List[RawFlashcardDataDTO], word_id: str
    ) -> List[FlashcardDTO]:
        word_text = raw_flashcards_data[0].word
        sentences_payload = [
            {
                "target_language_sentence": dto.target_language_sentence,
                "sentence_translation": dto.sentence_translation,
            }
            for dto in raw_flashcards_data
        ]

        user_prompt = json.dumps(
            {"word": word_text, "sentences": sentences_payload}, ensure_ascii=False
        )

        response = self.llm_adapter.generate_response(
            system=self.system_prompt,
            user=user_prompt,
        )

        if not response:
            raise ValueError("No response received from OpenAI")

        return [
            FlashcardDTO(
                id=str(uuid4()),
                word_id=word_id,
                front=item["front"],
                back=item["back"],
            )
            for item in json.loads(response)
        ]


# if __name__ == "__main__":
#     generate_flashcards_service = GenerateFlashcardsService()
#     dtos = [
#         RawFlashcardDataDTO(
#             word="das Haus",
#             target_language_sentence="Lass uns die Getränke im Haus vorbereiten.",
#             sentence_translation="Przygotujmy napoje w domu.",
#         ),
#         RawFlashcardDataDTO(
#             word="das Haus",
#             target_language_sentence="Das Haus ist rot.",
#             sentence_translation="Dom jest czerwony.",
#         ),
#         RawFlashcardDataDTO(
#             word="das Haus",
#             target_language_sentence="Wir tanzen die ganze Nacht im Haus.",
#             sentence_translation="Tańczymy całą noc w domu.",
#         ),
#     ]
#     flashcards = generate_flashcards_service.execute(
#         raw_flashcards_data=dtos, word_id=""
#     )

#     for flashcard in flashcards:
#         print(flashcard)
