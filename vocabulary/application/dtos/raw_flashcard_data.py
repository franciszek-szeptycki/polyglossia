from dataclasses import dataclass


@dataclass
class RawFlashcardDataDTO:
    word: str
    target_language_sentence: str
    sentence_translation: str
