from dataclasses import dataclass


@dataclass
class FlashcardDTO:
    id: str
    front: str
    back: str
