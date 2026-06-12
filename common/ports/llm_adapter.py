from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMAdapter(ABC):
    @abstractmethod
    def generate_response(
        self,
        *,
        system: str,
        user: str,
    ) -> str: ...

    @abstractmethod
    def prompt_json(self, *, user: str) -> dict: ...
