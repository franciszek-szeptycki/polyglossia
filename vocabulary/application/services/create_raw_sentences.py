import json
import os
import pathlib
from typing import List

from common.adapters.ollama_adapter import ollama_adapter
from common.ports.llm_adapter import LLMAdapter


class CreateRawSentencesService:
    def __init__(self, *, llm_adapter: LLMAdapter):
        self.llm_adapter: LLMAdapter = llm_adapter

        with open(self._get_prompt_path()) as file:
            self.system_prompt = file.read()

    def execute(self, *, word: str) -> List[str]:
        user_prompt = f"słowo: {word}"

        response = self.llm_adapter.generate_response(
            system=self.system_prompt,
            user=user_prompt,
        )

        if not response:
            raise ValueError("No response received from LLM")

        try:
            return json.loads(response)
        except json.decoder.JSONDecodeError as _:
            print(response)
            raise ValueError("Failed to parse response from LLM")

    def _get_prompt_path(self) -> str:
        return os.path.join(
            pathlib.Path(__file__).resolve().parent,
            "prompts",
            "create_raw_sentences.txt",
        )


if __name__ == "__main__":
    llm_adapter = ollama_adapter
    svc = CreateRawSentencesService(llm_adapter=ollama_adapter)
    sentences = svc.execute(word="Krankenheit")
    for sentence in sentences:
        print(sentence)
