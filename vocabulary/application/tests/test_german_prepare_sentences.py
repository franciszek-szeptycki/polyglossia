import json
import pathlib

from django.test import SimpleTestCase

from vocabulary.application.services.german import GermanFlashcardsService

FIXTURE_PATH = (
    pathlib.Path(__file__).resolve().parent.parent
    / "services"
    / "german.json"
)


class GermanFlashcardsServicePrepareSentencesTest(SimpleTestCase):
    def setUp(self):
        self.service = GermanFlashcardsService(llm=None)
        with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
            self.fixture = json.load(f)

    def test_prepare_sentences_replaces_word_with_translation(self):
        result = self.service.prepare_sentences(
            sentences=self.fixture["sentences"],
            forms=self.fixture["forms"],
            translated_words=self.fixture["translated_words"],
        )

        expected = [
            "Ich muss hier [ wysiąść ].",
            "Wann [ wysiadamy ] wir [ wysiadamy ]?",
            "Bitte vorne [ wysiadać ].",
            "Er will nicht [ wysiąść ].",
            "[ wysiadasz ] du an der nächsten [ wysiadasz ]?",
            "Können wir jetzt [ wysiąść ]?",
            "Lass uns schnell [ wysiądźmy ].",
        ]

        self.assertEqual(result, expected)

    def test_prepare_sentences_returns_same_number_of_items_as_input(self):
        result = self.service.prepare_sentences(
            sentences=self.fixture["sentences"],
            forms=self.fixture["forms"],
            translated_words=self.fixture["translated_words"],
        )

        self.assertEqual(len(result), len(self.fixture["sentences"]))
