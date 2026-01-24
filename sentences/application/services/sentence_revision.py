import json
from uuid import uuid4

from sentences.application.dtos.sentece import SentenceDTO
from sentences.application.dtos.sentence_revision import SentenceRevisionDTO
from sentences.infrastructure.adapters.openai_adapter import openai_adapter


class GetSentenceRevisionService:
    SYSTEM_PROMPT = """
    Jesteś nauczycielem języka niemieckiego. Twoim zadaniem jest sprawdzenie czy poniższe zdanie jest poprawne.
    Jeśli nie, popraw je. Spodziewaj się że uczeń ma poziom językowy B1.
    """

    def execute(self, *, sentence_dto: SentenceDTO) -> SentenceRevisionDTO:
        response = openai_adapter.generate_response(
            system="", user="What is the capital of France?"
        )

        if not response:
            raise ValueError("No response received from OpenAI")

        try:
            json_data = json.loads(response)
        except json.JSONDecodeError:
            json_data = {"raw_response": response}
        except Exception as e:
            raise ValueError(f"Error parsing response: {e}")

        return SentenceRevisionDTO(
            id=str(uuid4()),
            text=sentence_dto.text,
            revision=dict(json_data),
        )


get_sentence_revision_service = GetSentenceRevisionService()
