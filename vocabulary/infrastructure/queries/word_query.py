from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.infrastructure.models.word import Word


class WordQuery:
    @staticmethod
    def list():
        return Word.objects.filter(profile=get_profile_id())
