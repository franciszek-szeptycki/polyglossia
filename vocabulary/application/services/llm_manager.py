import json
import os
import pathlib
import re
from dataclasses import dataclass
from itertools import count
from typing import List

from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.raw_flashcard_data import RawFlashcardDataDTO
from vocabulary.application.dtos.word import WordDTO

TYPE_NOUN = "noun"
TYPE_VERB = "verb"
TYPE_ADJ = "adj"
TYPE_OTHER = "other"


@dataclass
class EvaFlashcard:
    back: str
    front: str


class LlmManager:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._error_dir = "./.tmp/llm_errors"
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "create_eva_flashcard": self._load_prompt("create_eva_flashcard.txt"),
        }

    def _initialize_error_counter(self) -> count:
        if not os.path.exists(self._error_dir):
            return count(1)

        existing_files = os.listdir(self._error_dir)
        indices = []

        for filename in existing_files:
            match = re.match(r"^(\d+)\.", filename)
            if match:
                indices.append(int(match.group(1)))

        next_idx = max(indices) + 1 if indices else 1
        return count(next_idx)

    def create_eva_flashcard(self, *, word: str) -> List[EvaFlashcard]:
        prompt_method = "create_eva_flashcard"

        system = self._prompts[prompt_method]
        user = f"słowo: {word}"

        response = self._generate(system=system, user=user)

        json_data = self._parse_json(response, prompt_method, system + user)

        return [
            EvaFlashcard(
                front=d["front"],
                back=d["back"],
            )
            for d in json_data
        ]

    def _generate(self, *, system: str, user: str) -> str:
        response = self.llm_adapter.generate_response(
            system=system,
            user=user,
        )

        if not response:
            raise ValueError("No response received from LLM")

        return response

    def _parse_json(self, response: str, method: str, request: str):
        try:
            return json.loads(response)
        except (json.decoder.JSONDecodeError, TypeError):
            self._store_error(method, request, response)
            raise ValueError(f"Failed to parse response from LLM in {method}")

    def _store_error(self, method: str, request: str, response: str):
        idx = next(self._error_counter)
        os.makedirs(self._error_dir, exist_ok=True)

        base = os.path.join(self._error_dir, f"{idx}.{method}")

        with open(f"{base}.request.txt", "w", encoding="utf-8") as f:
            f.write(request)

        with open(f"{base}.response.txt", "w", encoding="utf-8") as f:
            f.write(response)

    def _load_prompt(self, filename: str) -> str:
        base_dir = pathlib.Path(__file__).resolve().parent
        prompt_path = base_dir / "prompts" / filename

        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()


if __name__ == "__main__":
    # llm_adapter = ollama_adapter
    llm_adapter = openai_adapter
    mng = LlmManager(llm_adapter=llm_adapter)
    word = "einwerfen"

    try:
        flashcards = mng.create_eva_flashcard(word=word)
        for flashcard in flashcards:
            print(flashcard.front)
            print(flashcard.back)
            print("=" * 10)

    except Exception as e:
        print(f"Error occurred: {e}")
