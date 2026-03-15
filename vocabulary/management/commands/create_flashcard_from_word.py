from django.core.management.base import BaseCommand

from common.adapters.openai_adapter import OpenAIAdapter
from profiles.consts import Language
from vocabulary.domain.services.create_flashcards_service import (
    CreateFlaschardsService,
)
from vocabulary.infrastructure.adapters.prompt_manager import PromptManagersContainer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--word", type=str, required=True)

    def handle(self, *args, **options):
        word = options["word"]

        llm_adapter = OpenAIAdapter()
        prompt_mng_container = PromptManagersContainer(llm_adapter=llm_adapter)

        service = CreateFlaschardsService(
            prompt_managers=prompt_mng_container
        )

        flashcards = service.execute(word=word, language=Language.GERMAN)
        for flashcard in flashcards:
            print(flashcard)
            print(flashcard.front)
            print(flashcard.back)
            print("=" * 10)
