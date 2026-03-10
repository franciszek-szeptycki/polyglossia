from common.ports.llm_adapter import LLMAdapter
from vocabulary.application.dtos.word import WordDTO
from vocabulary.domain.ports.word_repository import WordRepositoryABC


class MockLlmAdapter(LLMAdapter):
    def __init__(self, raw_data: str):
        self.raw_data = raw_data

    def generate_response(self, *, system, user: str) -> str:
        return self.raw_data


class MockWordRepository(WordRepositoryABC):
    def __init__(self, words: list = []):
        self.words = words

    def create(self, dto: WordDTO) -> WordDTO:
        self.words.append(dto)
        return dto

    def get(self, id: str) -> WordDTO:
        for word in self.words:
            if word.id == id:
                return word
        raise Exception("No word with exact id")

    def generating_flash_cards_in_progress(self, *, word_id: str):
        pass

    def generating_flash_cards_done(self, *, word_id: str):
        pass

    def generating_flash_cards_failed(self, *, word_id: str):
        pass
