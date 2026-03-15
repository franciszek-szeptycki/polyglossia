from common.adapters.openai_adapter import OpenAIAdapter
from vocabulary.application.use_cases.create_flashcards_from_word_use_case import (
    GenerateFlashcardsForWordUseCase,
)
from vocabulary.application.use_cases.get_flashcard_data_to_export_use_case import (
    GetFlashcardDataToExportUseCase,
)
from vocabulary.domain.services.create_flashcards_service import (
    CreateFlaschardsService,
)
from vocabulary.infrastructure.adapters.prompt_manager import (
    PromptManagersContainer,
)
from vocabulary.infrastructure.repositories.flashcard_repository import (
    FlashcardRepository,
)
from vocabulary.infrastructure.repositories.word_repository import WordRepository


class DependencyContainer:
    def __init__(self):
        ##################
        #  REPOSITORIES  #
        ##################
        self.repository_word = WordRepository()
        self.repository_flashcard = FlashcardRepository()

        ##############
        #  ADAPTERS  #
        ##############
        self.adapter_llm = OpenAIAdapter()
        self.manager_prompt = PromptManagersContainer(llm_adapter=self.adapter_llm)

        ##############
        #  SERVICES  #
        ##############
        self.service_create_eva_flashcards = CreateFlaschardsService(prompt_managers=self.manager_prompt)

        ###############
        #  USE_CASES  #
        ###############
        self.use_case_generate_flashcards_for_word = GenerateFlashcardsForWordUseCase(
            word_repo=self.repository_word,
            flashcard_repo=self.repository_flashcard,
            llm_adapter=self.adapter_llm,
        )
        self.use_case_get_flashcard_data_to_export = GetFlashcardDataToExportUseCase(
            flashcard_repo=self.repository_flashcard,
        )

container = DependencyContainer()
