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
from vocabulary.application.managers.prompt_manager import PromptManager


@dataclass
class EvaFlashcard:
    back: str
    front: str


class EvaFlashcardBuilder:
    def __init__(self, *, prompt_manager: PromptManager):
        self._prompt_manager = prompt_manager

        self._raw_sentence = ""
        self._front = ""
        self._back = ""
        self._additional_info = ""

    def add_word(self, word: str) -> None:
        self._word = word

    def add_raw_sentence(self, raw_sentence: str) -> None:
        self._raw_sentence = raw_sentence

    def generate_draft(self) -> None:
        data = self._prompt_manager.create_eva_flashcard(
            word=self._word, sentence=self._raw_sentence
        )
        self._front = data["front"]
        self._back = data["back"]

    def generate_additional_info(self) -> None:
        data = self._prompt_manager.get_additional_word_info(
            word=self._word,
            raw_sentence=self._raw_sentence,
        )
        self._additional_info = data["additional_data"]

    def build(self) -> "EvaFlashcard":
        return EvaFlashcard(
            front=self._front,
            back=f"{self._back} - {self._additional_info}",
        )


class CreateEvaFlaschardsService:
    def __init__(self, *, prompt_manager: PromptManager):
        self._prompt_manager = prompt_manager

    def execute(self, *, word: str) -> List["EvaFlashcard"]:
        raw_sentences = self._prompt_manager.create_raw_sentences(word=word)

        filtered_sentences = self._prompt_manager.filter_raw_sentences(
            word=word, sentences=raw_sentences
        )

        eva_flashcards = []
        for sentence in filtered_sentences:
            builder = EvaFlashcardBuilder(prompt_manager=self._prompt_manager)

            builder.add_word(word=word)
            builder.add_raw_sentence(raw_sentence=sentence)
            builder.generate_draft()
            builder.generate_additional_info()

            eva_flashcards.append(builder.build())

        return eva_flashcards
