from dataclasses import dataclass


@dataclass
class SentenceRevisionDTO:
    id: str
    original_text: str
    translated_text: str
    revision: dict
