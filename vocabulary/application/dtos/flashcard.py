from dataclasses import dataclass
from datetime import datetime
from optparse import Option
from typing import Optional

from attrs import frozen


@frozen(kw_only=True)
class Flashcard:
    front: str
    back: str


@dataclass
class FlashcardDTO:
    word_id: str
    front: str
    back: str
    id: Optional[str] = None
    is_active: Optional[bool] = None
    exported_at: Optional[datetime] = None
    profile_id: Optional[int] = None
