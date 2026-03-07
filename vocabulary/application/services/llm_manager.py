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

TYPE_NOUN = "noun"
TYPE_VERB = "verb"
TYPE_ADJ = "adj"
TYPE_OTHER = "other"


class LlmManager:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._error_dir = "./tmp/llm_errors"
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "create_sentences": self._load_prompt("create_sentences.txt"),
            "filter_sentences": self._load_prompt("filter_sentences.txt"),
            "is_word_in_sentence": self._load_prompt("is_word_in_sentence.txt"),
            "determine_word_type": self._load_prompt("determine_word_type.txt"),
            "create_sentences.noun": self._load_prompt("create_sentences.noun.txt"),
            "create_sentences.verb": self._load_prompt("create_sentences.verb.txt"),
            "create_sentences.adj": self._load_prompt("create_sentences.adj.txt"),
            "create_sentences.other": self._load_prompt("create_sentences.other.txt"),
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

    def create_sentences(self, *, word: str, word_type: str) -> List[str]:
        user_prompt = f"słowo: {word}"

        if word_type not in ("noun", "verb", "adj", "other"):
            raise ValueError(f"Invalid word type: {word_type}")

        prompt_method = f"create_sentences.{word_type}"
        response = self._generate(
            system=self._prompts[prompt_method],
            user=user_prompt,
        )

        return self._parse_json(response, prompt_method, user_prompt)

    # def filter_sentences(self, *, word: str, sentences: List[str]) -> List[str]:
    #     filtered_sentences = []
    #     for sentence in sentences:
    #         if self.is_word_in_sentence(word=word, sentence=sentence):
    #             filtered_sentences.append(sentence)
    #     return filtered_sentences

    def determine_word_type(self, *, word: str) -> str:
        user_prompt = f"słowo: {word}"

        response = self._generate(
            system=self._prompts["determine_word_type"],
            user=user_prompt,
        )
        if TYPE_NOUN in response:
            return TYPE_NOUN
        if TYPE_VERB in response:
            return TYPE_VERB
        if TYPE_ADJ in response:
            return TYPE_ADJ
        return TYPE_OTHER

    # def is_word_in_sentence(self, *, word: str, sentence: str) -> bool:
    #     user_prompt = f"słowo: {word}\nzdanie: {sentence}\n"

    #     response = self._generate(
    #         system=self._prompts["is_word_in_sentence"],
    #         user=user_prompt,
    #     )
    #     print(response)
    #     print("-" * 10)
    #     if "TAK" in response:
    #         return True
    #     if "NIE" in response:
    #         return False
    #     raise ValueError(f"Unexpected response from LLM: {response}")

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
    word = "wissenschaftlich"

    try:
        word_type = mng.determine_word_type(word=word)
        print(f"WORD_TYPE: {word_type}")

        sentences = mng.create_sentences(word=word, word_type=word_type)
        for s in sentences:
            print(s)

    except Exception as e:
        print(f"Error occurred: {e}")
