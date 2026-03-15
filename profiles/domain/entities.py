from dataclasses import dataclass

@dataclass
class ProfileDTO:
    id: int
    user_id: int
    language: str
    is_active: bool
