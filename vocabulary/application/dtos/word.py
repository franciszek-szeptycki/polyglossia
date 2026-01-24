from dataclasses import dataclass


@dataclass
class WordDTO:
    id: str
    text: str
    context: str
