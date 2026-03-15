from dataclasses import dataclass
from typing import List

from profiles.consts import Language
from vocabulary.infrastructure.adapters.prompt_manager import PromptManager, PromptManagersContainer
from tqdm import tqdm


@dataclass
class EvaFlashcard:
    back: str
    front: str


class CreateFlaschardsService:
    def __init__(self, *, prompt_managers: PromptManagersContainer):
        self._prompt_managers = prompt_managers

    def _get_prompt_manager(self, *, language: str) -> PromptManager:
        return {
            Language.GERMAN.value: self._prompt_managers.language_de,
            Language.SPANISH.value: self._prompt_managers.language_es,
            Language.ENGLISH.value: self._prompt_managers.language_en,
        }[language]

    def execute(self, *, word: str, language: str) -> List[EvaFlashcard]:
        prompt_manager = self._get_prompt_manager(language=language)

        with tqdm(total=2, desc=f"Processing '{word}'") as progress_bar:

            sentences = prompt_manager.create_raw_sentences(word=word)
            progress_bar.update(1)

            flashcards = []
            for item in prompt_manager.create_eva_flashcards(word=word, sentences=sentences):
                flashcards.append(EvaFlashcard(
                    front=item["front"],
                    back=item["back"],
                ))
            progress_bar.update(1)

            return flashcards
