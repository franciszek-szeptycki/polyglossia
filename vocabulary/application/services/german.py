import re
from logging import getLogger
from typing import List

import json

from common.adapters.openai_adapter import OpenAIAdapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.flashcard import Flashcard
from vocabulary.application.services.german_prompts import GermanPrompts

logger = getLogger(__name__)


class GermanFlashcardsService:
    def __init__(self, llm: LLMAdapter):
        self.llm: LLMAdapter = llm

    def execute(self, *, word: str) -> List[Flashcard]:
        try:
            # STEP 1
            logger.info(f"GermanFlashcardsService::STEP 1 - word='{word}'")
            sentences_prompt = GermanPrompts.sentences(word=word)
            sentences = self.llm.prompt_json(user=sentences_prompt).get("sentences", [])

            # STEP 2
            logger.info(f"GermanFlashcardsService::STEP 2 - word='{word}'")
            forms_prompt = GermanPrompts.word_forms(sentences=sentences, word=word)
            forms = self.llm.prompt_json(user=forms_prompt).get("forms", [])

            # STEP 3
            logger.info(f"GermanFlashcardsService::STEP 3 - word='{word}'")
            translation_prompt = GermanPrompts.translate(
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
            logger.info(f"GermanFlashcardsService::STEP 4 - word='{word}'")
            replaced_sentences = self.prepare_sentences(
                sentences=sentences, forms=forms, translated_words=translated_words
            )

            # STEP 5
            logger.info(f"GermanFlashcardsService::STEP 5 - word='{word}'")
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
            logger.error(f"Error in GermanFlashcardsService: {e}")
            raise e

    def prepare_sentences(self, *, sentences, forms, translated_words) -> List[str]:
        replaced_sentences = []
        for sentence, form, translated_word in zip(
            sentences, forms, translated_words
        ):
            replaced_sentence = sentence
            if " ... " not in form:
                safe_word = re.escape(form)
                replaced_sentence = re.sub(safe_word, f"[ {translated_word} ]", replaced_sentence, flags=re.IGNORECASE)
            else:
                for word_part in form.split(" ... "):
                    safe_word = re.escape(word_part)
                    replaced_sentence = re.sub(safe_word, f"[ {translated_word} ]", replaced_sentence, flags=re.IGNORECASE)

            replaced_sentences.append(replaced_sentence)
        return replaced_sentences


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    GermanFlashcardsService(llm=OpenAIAdapter()).execute(word="spreche")
