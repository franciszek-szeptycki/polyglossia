from typing import List

from common.adapters.openai_adapter import OpenAIAdapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import Flashcard
from vocabulary.application.services.spanish_prompts import SpanishPrompts


class SpanishFlashcardsService:
    def __init__(self, llm: LLMAdapter):
        self.llm: LLMAdapter = llm

    def execute(self, *, word: str) -> List[Flashcard]:
        try:
            # STEP 1
            sentences_prompt = SpanishPrompts.sentences(word=word)
            sentences = self.llm.prompt_json(user=sentences_prompt).get("sentences", [])

            # STEP 2
            forms_prompt = SpanishPrompts.word_forms(sentences=sentences, word=word)
            forms = self.llm.prompt_json(user=forms_prompt).get("forms", [])

            # STEP 3
            translation_prompt = SpanishPrompts.translate(
                data=list(zip(sentences, forms))
            )
            translations = self.llm.prompt_json(user=translation_prompt).get(
                "translations", []
            )
            translated_sentences = [
                translation["sentence"] for translation in translations
            ]
            translated_words = [translation["word"] for translation in translations]

            # STEP 4
            replaced_sentences = []
            for sentence, form, translated_word in zip(
                sentences, forms, translated_words
            ):
                replaced_sentece = sentence.replace(form, f"[ {translated_word} ]")
                replaced_sentences.append(replaced_sentece)
            print(replaced_sentences)

            # STEP 5
            flashcards = []
            for replaced_sentece, translated_sentence, word_form in zip(
                replaced_sentences, translated_sentences, forms
            ):
                flashcard = Flashcard(
                    front=replaced_sentece,
                    back=f"{word_form} ({translated_sentence})",
                )
                flashcards.append(flashcard)
            return flashcards
        except Exception as e:
            raise e


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    SpanishFlashcardsService(llm=OpenAIAdapter()).execute(word="hablo")
