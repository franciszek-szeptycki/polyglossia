import json
from uuid import uuid4

from common.adapters.openai_adapter import openai_adapter
from sentences.application.dtos.sentence import SentenceDTO
from sentences.application.dtos.sentence_revision import SentenceRevisionDTO


class GetSentenceRevisionService:
    SYSTEM_PROMPT = """
    Jesteś nauczycielem języka niemieckiego.
    Twoim zadaniem jest sprawdzenie czy poniższe zdanie zostało poprawnie przetłumaczone z języka polskiego na niemiecki.
    Spodziewaj się że uczeń ma poziom językowy B1.

    Wydaj opinię w formacie JSON, bez żadnych znaków przed czy po.

    np:
    pl: Zostaję w domu, bo pada deszcz.
    de: Ich bleibe zu Hause, weil regnet es.
    {
        "correct": false,
        "corrected_text": "Ich bleibe zu Hause, weil es regnet.",
        "reason": "Problem jest w kolejności wyrazów w zdaniu podrzędnym (po „weil”). W zdaniu podrzędnym czasownik idzie na koniec zdania. „Es” jest podmiotem, więc czasownik „regnet” musi znaleźć się na końcu."
    }

    lub:
    pl: Teraz jem, ponieważ jestem głodny.
    de: Ich esse jetzt, denn ich habe Hunger
    {
        "correct": true,
        "corrected_text": "",
        "reason": ""
    }

    lub:
    pl: Idę do kina, bo dziś nie ma czasu.
    de: Ich gehe ins Kino nicht
    {
        "correct": false,
        "corrected_text": "Ich gehe nicht ins Kino",
        "reason": "języku niemieckim słowo „nicht” (nie) zwykle stoi przed tym, co chcemy zaprzeczyć, a w przypadku całego zdania (zaprzeczenie całej czynności) „nicht” stoi na końcu zdania w czasie teraźniejszym."
    }
    """

    def execute(self, *, sentence_dto: SentenceDTO) -> SentenceRevisionDTO:
        user_prompt = f"""
        pl: {sentence_dto.original_text}
        de: {sentence_dto.translated_text}
        """
        response = openai_adapter.generate_response(
            system=self.SYSTEM_PROMPT, user=user_prompt
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
            original_text=sentence_dto.original_text,
            translated_text=sentence_dto.translated_text,
            revision=dict(json_data),
        )


get_sentence_revision_service = GetSentenceRevisionService()
