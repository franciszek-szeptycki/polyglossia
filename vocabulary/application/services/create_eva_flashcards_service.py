import concurrent.futures
import json
import os
import pathlib
import re
from dataclasses import dataclass
from itertools import count
from typing import Any, Callable, List

from tqdm import tqdm

from common.ports.llm_adapter import LLMAdapter


@dataclass
class EvaFlashcard:
    back: str
    front: str


class CreateEvaFlaschardsService:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter = llm_adapter
        self._error_dir = "./.tmp/llm_errors"
        self._language = "de"
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "1.create_raw_sentences": self._load_prompt("1.create_raw_sentences.txt"),
            "2.filter_raw_sentences": self._load_prompt("2.filter_raw_sentences.txt"),
            "3.replace_in_eva_style": self._load_prompt("3.replace_in_eva_style.txt"),
        }

    def execute(self, *, word: str) -> List["EvaFlashcard"]:
        raw_sentences = self._create_raw_sentences(word=word)

        filtered_sentences = self._filter_raw_sentences(
            word=word, sentences=raw_sentences
        )

        for i, fs in enumerate(filtered_sentences):
            tqdm.write(f'{i}. "{fs}"')

        eva_flashcards: List["EvaFlashcard"] = [
            EvaFlashcard(front=item["front"], back=item["back"])
            for item in self._multithreaded_execute(
                func=self._create_eva_flashcard,
                items=filtered_sentences,
                word=word,
            )
        ]

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

    def _create_eva_flashcard(self, *, word: str, item: str) -> dict:
        prompt_method = "3.replace_in_eva_style"
        system_prompt = self._prompts[prompt_method]
        user_prompt = f"Słowo: {word}\nZdanie: {item}"

        response = self._generate(system=system_prompt, user=user_prompt)

        return self._parse_json(response, prompt_method, system_prompt + user_prompt)

    def _replace_in_eva_style(self, *, word: str, sentence: str) -> EvaFlashcard:
        prompt_method = "3.replace_in_eva_style"
        system_prompt = self._prompts[prompt_method]
        user_prompt = f"Słowo: {word}\nZdanie: {sentence}"

        response = self._generate(system=system_prompt, user=user_prompt)

        json_data = self._parse_json(
            response, prompt_method, system_prompt + user_prompt
        )

        return EvaFlashcard(
            front=json_data["front"],
            back=json_data["back"],
        )

    #############
    #  Helpers  #
    #############

    def _multithreaded_execute(
        self, *, func: Callable, items: List[Any], **kwargs
    ) -> List[Any]:
        results: List[Any] = []
        with tqdm(total=len(items), position=0, leave=False) as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_item = {
                    executor.submit(func, item=item, **kwargs): item for item in items
                }
                for future in concurrent.futures.as_completed(future_to_item):
                    card = future.result()
                    results.append(card)
                    pbar.update(1)
        return results

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
        prompt_path = base_dir / "prompts" / self._language / filename

        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
