import json
import os
import pathlib
import re
from itertools import count
from typing import  Any, Dict, List
from profiles.consts import Language

from common.ports.llm_adapter import LLMAdapter


class PromptManager:
    def __init__(self, *, llm_adapter: LLMAdapter, language: str):
        self._llm_adapter = llm_adapter
        self._error_dir = "./.tmp/llm_errors"
        self._language = language
        self._error_counter = self._initialize_error_counter()

        self._prompts = {
            "1.create_raw_sentences": self._load_prompt("1.create_raw_sentences.txt"),
            "2.replace_in_eva_style": self._load_prompt("2.replace_in_eva_style.txt"),
        }

    def create_raw_sentences(self, *, word: str) -> List[str]:
        prompt_method = "1.create_raw_sentences"
        prompt = self._prompts[prompt_method].replace("__REPLACE_WORD__", word)

        response = self._generate(prompt=prompt)

        return self._parse_json(
            response=response,
            method=prompt_method,
            request=prompt,
        )["sentences"]

    def create_eva_flashcards(self, *, word: str, sentences: List[str]) -> List[dict]:
        prompt_method = "2.replace_in_eva_style"

        prompt = self._prompts[prompt_method]
        prompt = prompt.replace("__REPLACE_SENTENCES__", "\n".join(sentences))
        prompt = prompt.replace("__REPLACE_WORD__", word)

        response = self._generate(prompt=prompt)

        return self._parse_json(
            response=response,
            method=prompt_method,
            request=prompt,
        )["flashcards"]

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

    # def _generate(self, *, system: str, user: str) -> str:
    def _generate(self, *, prompt: str) -> str:
        response = self._llm_adapter.generate_response(
            system="",
            user=prompt,
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
        BASE_DIR = pathlib.Path(__file__).resolve().parent
        prompt_path = BASE_DIR / "prompts"  / self._language / filename

        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()


class PromptManagersContainer:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.language_de = PromptManager(llm_adapter=llm_adapter, language=Language.GERMAN.value)
        self.language_es = PromptManager(llm_adapter=llm_adapter, language=Language.SPANISH.value)
        self.language_en = PromptManager(llm_adapter=llm_adapter, language=Language.ENGLISH.value)
