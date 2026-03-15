from dataclasses import dataclass

from profiles.consts import Language

@dataclass(frozen=True)
class ProfileDTO:
    id: int
    user_id: int
    language: Language
