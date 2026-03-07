import json
import os
import pathlib
import re
from itertools import count
from typing import List

from common.adapters.ollama_adapter import ollama_adapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.raw_flashcard_data import RawFlashcardDataDTO
from vocabulary.application.dtos.word import WordDTO


class LlmManager:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._error_dir = "./tmp/llm_errors"
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "create_sentences": self._load_prompt("create_raw_sentences.txt"),
            "filter_sentences": self._load_prompt("filter_sentences.txt"),
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

    def create_sentences(self, *, word: str) -> List[str]:
        user_prompt = f"słowo: {word}"

        response = self._generate(
            system=self._prompts["create_sentences"],
            user=user_prompt,
        )

        return self._parse_json(response, "create_sentences", user_prompt)

    def filter_sentences(self, *, word: str, sentences: List[str]) -> List[str]:
        user_prompt = f"słowo: {word}\nzdania:\n"
        for sentence in sentences:
            user_prompt += f"{sentence}\n"

        response = self._generate(
            system=self._prompts["filter_sentences"],
            user=user_prompt,
        )

        return self._parse_json(response, "filter_sentences", user_prompt)

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
    mng = LlmManager(llm_adapter=ollama_adapter)

    try:
        res = mng.create_sentences(word="Krankenheit")
        for s in res:
            print(s)
    except Exception as e:
        print(f"Error occurred: {e}")
