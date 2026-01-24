from dataclasses import dataclass


@dataclass
class SentenceDTO:
    original_text: str
    translated_text: str
