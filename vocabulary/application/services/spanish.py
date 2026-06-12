from typing import List

from common.adapters.openai_adapter import OpenAIAdapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import Flashcard
from vocabulary.application.services.spanish_vars import SpanishPrompts


class SpanishFlashcardsService:
    def __init__(self, llm: LLMAdapter):
        self.llm: LLMAdapter = llm

    def execute(self, *, word: str) -> List[Flashcard]:
        sentences_prompt = SpanishPrompts.sentences(word=word)
        sentences = self.llm.prompt_json(user=sentences_prompt).get("sentences", [])
        print(sentences)
        pass


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    SpanishFlashcardsService(llm=OpenAIAdapter()).execute(word="hola")
