from common.adapters.ollama_adapter import OllamaAdapter
from common.adapters.openai_adapter import OpenAIAdapter
from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.managers.prompt_manager import PromptManagersContainer
from vocabulary.application.ports.word_repository import WordRepositoryABC
from vocabulary.application.services.create_eva_flashcards_service import (
    CreateEvaFlaschardsService,
)
from vocabulary.application.use_cases.create_flashcards_from_word_use_case import (
    GenerateFlashcardsForWordUseCase,
)
from vocabulary.application.use_cases.get_flashcard_data_to_export_use_case import (
    GetFlashcardDataToExportUseCase,
)
from vocabulary.infrastructure.repositories.flashcard_repository import (
    FlashcardRepository,
)
from vocabulary.infrastructure.repositories.word_repository import WordRepository


class DependencyContainer:
    def __init__(self, *, offline: bool = False):
        self._offline = offline

        self._word_repository: WordRepositoryABC
        self._flashcard_repository: FlashcardRepository
        self._llm_adapter: LLMAdapter
        self._prompt_managers: PromptManagersContainer
        self._service_create_eva_flashcards: CreateEvaFlaschardsService
        self._use_case_generate_flashcards_for_word: GenerateFlashcardsForWordUseCase
        self._use_case_get_flashcard_data_to_export: GetFlashcardDataToExportUseCase

    ##############
    #  ADAPTERS  #
    ##############

    @property
    def repository_word(self):
        if self._word_repository:
            return self._word_repository
        self._word_repository = WordRepository()
        return self._word_repository

    @property
    def repository_flashcard(self):
        if self._flashcard_repository:
            return self._flashcard_repository
        self._flashcard_repository = FlashcardRepository()
        return self._flashcard_repository

    @property
    def adapter_llm(self):
        if self._llm_adapter:
            return self._llm_adapter

        if self._offline:
            self._llm_adapter = OllamaAdapter()
        else:
            self._llm_adapter = OpenAIAdapter()

        return self._llm_adapter

    #############
    #  HELPERS  #
    #############

    @property
    def manager_prompt(self):
        if self._prompt_managers:
            return self._prompt_managers
        self._prompt_managers = PromptManagersContainer(llm_adapter=self._llm_adapter)
        return self._prompt_managers

    ##############
    #  SERVICES  #
    ##############

    @property
    def service_create_eva_flashcards_de(self):
        if not self._create_eva_flashcards_service:
            self._create_eva_flashcards_service = CreateEvaFlaschardsService(
                prompt_manager=self._prompt_managers.language_de
            )
        return self._create_eva_flashcards_service

    ###############
    #  USE CASES  #
    ###############

    @property
    def use_case_generate_flashcards_for_word(self):
        if not self._use_case_generate_flashcards_for_word:
            self._use_case_generate_flashcards_for_word = (
                GenerateFlashcardsForWordUseCase(
                    word_repo=self.repository_word,
                    flashcard_repo=self.repository_flashcard,
                    llm_adapter=self.adapter_llm,
                )
            )
        return self._use_case_generate_flashcards_for_word

    @property
    def use_case_get_flashcard_data_to_export(self):
        if not self._use_case_get_flashcard_data_to_export:
            self._use_case_get_flashcard_data_to_export = (
                GetFlashcardDataToExportUseCase(
                    flashcard_repo=self.repository_flashcard,
                )
            )
        return self._use_case_get_flashcard_data_to_export


container = DependencyContainer()
