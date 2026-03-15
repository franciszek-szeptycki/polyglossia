from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List

from tqdm import tqdm

from profiles.consts import Language
from vocabulary.infrastructure.adapters.prompt_manager import PromptManager, PromptManagersContainer


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
    def __init__(self, *, prompt_managers: PromptManagersContainer):
        self._prompt_managers = prompt_managers

    def _get_prompt_manager(self, *, language: Language) -> PromptManager:
        return {
            Language.GERMAN: self._prompt_managers.language_de,
            Language.SPANISH: self._prompt_managers.language_es,
            Language.ENGLISH: self._prompt_managers.language_en,
        }[language]

    def execute(self, *, word: str, language: Language) -> List[EvaFlashcard]:

        prompt_manager = self._get_prompt_manager(language=language)

        raw_sentences = prompt_manager.create_raw_sentences(word=word)

        filtered_sentences = prompt_manager.filter_raw_sentences(
            word=word, sentences=raw_sentences
        )

        num_sentences = len(filtered_sentences)
        if num_sentences == 0:
            return []

        eva_flashcards: List[EvaFlashcard] = []

        def process_sentence(sentence: str) -> "EvaFlashcard":
            builder = EvaFlashcardBuilder(prompt_manager=prompt_manager)
            builder.add_word(word=word)
            builder.add_raw_sentence(raw_sentence=sentence)
            builder.generate_draft()
            builder.generate_additional_info()
            return builder.build()

        with ThreadPoolExecutor() as executor:
            future_to_sentence = {
                executor.submit(process_sentence, s): s for s in filtered_sentences
            }

            for future in as_completed(future_to_sentence):
                card = future.result()
                eva_flashcards.append(card)

        return eva_flashcards
