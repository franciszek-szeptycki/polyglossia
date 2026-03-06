from unittest import TestCase

from vocabulary.application.dtos.word import WordDTO
from vocabulary.application.tests.mocks import MockLlmAdapter, MockWordRepository
from vocabulary.application.use_cases.create_flashcards_from_word import (
    GenerateFlashcardsForWordUseCase,
)


class TestGenerateFlashcardsForWord(TestCase):
    def test_execute(self):
        word_repo = MockWordRepository(
            [
                WordDTO(id="id", text="Krankheit"),
            ]
        )
        mock_llm_adapter = MockLlmAdapter(
            raw_data="""[
            "Sie haben eine Krankheit",
            "Die Krankheit ist nicht ernst.",
            "Ich habe einen Kurzurlaub wegen Krankheit.",
            "Krankenheiten sind nicht angenehm.",
            "Die Krankheitsstatistik nimmt zu.",
            "Was für ein komisches Gefühl, krank sein!",
            "Leider habe ich krank geschrieben.",
            "Ich bin sehr krank heute",
            "Die Krankenbehandlung ist wichtig.",
            "Erkrankte sollten auf sich selbst achten."
            ]"""
        )

        gffw_use_case = GenerateFlashcardsForWordUseCase(
            word_repo=word_repo, llm_adapter=mock_llm_adapter
        )

        result = gffw_use_case.execute(word_id="id")
        print(result)
