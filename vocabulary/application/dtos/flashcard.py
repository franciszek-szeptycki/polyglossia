from dataclasses import dataclass


@dataclass
class FlashcardDTO:
    id: str
    word_id: str
    front: str
    back: str
    is_active: bool
