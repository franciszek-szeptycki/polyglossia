from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FlashcardDTO:
    word_id: str
    front: str
    back: str
    id: Optional[str] = None
    is_active: Optional[bool] = None
    exported_at: Optional[datetime] = None
