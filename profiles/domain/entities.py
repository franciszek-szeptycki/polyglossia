from dataclasses import dataclass

from profiles.consts import Language

@dataclass
class ProfileDTO:
    id: int
    user_id: int
    language: Language
    is_active: bool
