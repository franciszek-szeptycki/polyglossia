from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FlashcardDTO:
    id: str
    word_id: str
    front: str
    back: str
    is_active: Optional[bool] = None
    exported_at: Optional[datetime] = None
