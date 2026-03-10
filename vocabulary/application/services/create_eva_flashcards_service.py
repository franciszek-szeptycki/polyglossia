from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List

from tqdm import tqdm

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
        with tqdm(total=100, desc=f"Word: {word}", unit="%") as pbar:
            raw_sentences = self._prompt_manager.create_raw_sentences(word=word)
            pbar.update(25)

            filtered_sentences = self._prompt_manager.filter_raw_sentences(
                word=word, sentences=raw_sentences
            )
            pbar.update(25)

            num_sentences = len(filtered_sentences)
            if num_sentences == 0:
                pbar.update(50)
                return []

            eva_flashcards = []
            step = 25 // num_sentences

            def process_sentence(sentence: str) -> "EvaFlashcard":
                builder = EvaFlashcardBuilder(prompt_manager=self._prompt_manager)
                builder.add_word(word=word)
                builder.add_raw_sentence(raw_sentence=sentence)

                builder.generate_draft()
                pbar.update(step)

                builder.generate_additional_info()
                pbar.update(step)

                return builder.build()

            with ThreadPoolExecutor() as executor:
                # Używamy dict do śledzenia tasków
                future_to_sentence = {
                    executor.submit(process_sentence, s): s for s in filtered_sentences
                }

                for future in as_completed(future_to_sentence):
                    try:
                        card = future.result()
                        eva_flashcards.append(card)
                    except Exception:
                        # Jeśli jeden padnie, dopychamy jego brakujący progress
                        pbar.update(step * 2)

            # Finalizacja do 100%
            if pbar.n < 100:
                pbar.update(100 - pbar.n)

            return eva_flashcards
