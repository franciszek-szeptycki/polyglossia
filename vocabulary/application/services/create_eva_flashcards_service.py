import json
import os
import pathlib
import re
from dataclasses import dataclass
from itertools import count
from typing import List

from tqdm import tqdm

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


class CreateEvaFlaschardsService:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._error_dir = "./.tmp/llm_errors"
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "1.create_raw_sentences": self._load_prompt("1.create_raw_sentences.txt"),
            "2.filter_raw_sentences": self._load_prompt("2.filter_raw_sentences.txt"),
            "3.replace_in_eva_style": self._load_prompt("3.replace_in_eva_style.txt"),
        }

    def execute(self, *, word: str) -> List["EvaFlashcard"]:
        with tqdm(total=3, position=0, leave=False) as pbar:
            raw_sentences = self._create_raw_sentences(word=word)
            pbar.update(1)

            filtered_sentences = self._filter_raw_sentences(
                word=word, sentences=raw_sentences
            )
            for i, fs in enumerate(filtered_sentences):
                tqdm.write(f'{i}. "{fs}"')
            pbar.update(1)

            eva_flashcards = self._replace_in_eva_style(
                word=word, sentences=filtered_sentences
            )
            for card in eva_flashcards:
                tqdm.write(str(card))
            pbar.update(1)

        return eva_flashcards

    def _create_raw_sentences(self, *, word: str) -> List[str]:
        prompt_method = "1.create_raw_sentences"
        system_prompt = self._prompts[prompt_method]
        user_prompt = f"słowo: {word}"

        response = self._generate(system=system_prompt, user=user_prompt)

        return self._parse_json(response, prompt_method, system_prompt + user_prompt)

    def _filter_raw_sentences(self, *, word: str, sentences: List[str]) -> List[str]:
        prompt_method = "2.filter_raw_sentences"
        system_prompt = self._prompts[prompt_method]
        user_prompt = f"Słowo: {word}\nZdania:\n" + "\n".join(sentences)

        response = self._generate(system=system_prompt, user=user_prompt)

        return self._parse_json(response, prompt_method, system_prompt + user_prompt)

    def _replace_in_eva_style(
        self, *, word: str, sentences: List[str]
    ) -> List[EvaFlashcard]:
        prompt_method = "3.replace_in_eva_style"
        system_prompt = self._prompts[prompt_method]
        user_prompt = f"Słowo: {word}\nZdania:\n" + "\n".join(sentences)

        response = self._generate(system=system_prompt, user=user_prompt)

        json_data = self._parse_json(
            response, prompt_method, system_prompt + user_prompt
        )

        return [
            EvaFlashcard(
                front=d["front"],
                back=d["back"],
            )
            for d in json_data
        ]

    #############
    #  Helpers  #
    #############

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
