from django.core.management.base import BaseCommand

from common.adapters.ollama_adapter import ollama_adapter
from common.adapters.openai_adapter import openai_adapter
from vocabulary.application.services.create_eva_flashcards_service import (
    CreateEvaFlaschardsService,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("word", type=str)

    def handle(self, *args, **options):
        word = options["word"]

        llm_adapter = ollama_adapter
        # llm_adapter = openai_adapter
        service = CreateEvaFlaschardsService(llm_adapter=llm_adapter)

        flashcards = service.execute(word=word)
        # for flashcard in flashcards:
        #     print(flashcard.front)
        #     print(flashcard.back)
        #     print("=" * 10)
