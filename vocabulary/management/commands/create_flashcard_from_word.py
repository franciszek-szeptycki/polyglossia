from django.core.management.base import BaseCommand

from common.adapters.openai_adapter import OpenAIAdapter
from vocabulary.application.managers.prompt_manager import PromptManagersContainer
from vocabulary.application.services.create_eva_flashcards_service import (
    CreateEvaFlaschardsService,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("word", type=str)

    def handle(self, *args, **options):
        word = options["word"]

        llm_adapter = OpenAIAdapter()
        prompt_mng_container = PromptManagersContainer(llm_adapter=llm_adapter)

        service = CreateEvaFlaschardsService(
            prompt_manager=prompt_mng_container.language_de
        )

        flashcards = service.execute(word=word)
        for flashcard in flashcards:
            print(flashcard)
            print(flashcard.front)
            print(flashcard.back)
            print("=" * 10)
