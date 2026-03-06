from dataclasses import dataclass
from typing import Optional


@dataclass
class WordDTO:
    id: str
    text: str
    context: str
    user_id: Optional[int] = None
