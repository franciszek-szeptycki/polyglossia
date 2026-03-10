from abc import ABC, abstractmethod


class LLMAdapter(ABC):
    @abstractmethod
    def generate_response(
        self,
        *,
        system: str,
        user: str,
    ) -> str: ...
