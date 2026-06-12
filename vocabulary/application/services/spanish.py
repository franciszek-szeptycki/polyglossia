from typing import List

from common.adapters.openai_adapter import OpenAIAdapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import Flashcard
from vocabulary.application.services.spanish_prompts import SpanishPrompts


class SpanishFlashcardsService:
    def __init__(self, llm: LLMAdapter):
        self.llm: LLMAdapter = llm

    def execute(self, *, word: str) -> List[Flashcard]:
        # STEP 1
        sentences_prompt = SpanishPrompts.sentences(word=word)
        sentences = self.llm.prompt_json(user=sentences_prompt).get("sentences", [])
        print(sentences)

        # STEP 2
        forms_prompt = SpanishPrompts.word_forms(sentences=sentences, word=word)
        forms = self.llm.prompt_json(user=forms_prompt).get("forms", [])
        print(forms)

        # STEP 3
        translation_prompt = SpanishPrompts.translate(data=list(zip(sentences, forms)))
        translations = self.llm.prompt_json(user=translation_prompt).get(
            "translations", []
        )
        print(translations)

        # STEP 4
        replaced_sentences = []
        for sentence, form in zip(sentences, forms):
            replaced_sentece = sentence.replace(form, f"[ {form} ]")
            replaced_sentences.append(replaced_sentece)
        print(replaced_sentences)

        # STEP 5
        flashcards = []
        for replaced_sentece, translation, word_form in zip(
            replaced_sentences, translations, forms
        ):
            flashcard = Flashcard(
                front=replaced_sentece,
                back=f"{word_form}<br>{translation}",
            )
            flashcards.append(flashcard)
        return flashcards


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    SpanishFlashcardsService(llm=OpenAIAdapter()).execute(word="hablo")
