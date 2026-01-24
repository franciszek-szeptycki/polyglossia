from dataclasses import dataclass


@dataclass
class SentenceRevisionDTO:
    id: str
    text: str
    revision: dict
