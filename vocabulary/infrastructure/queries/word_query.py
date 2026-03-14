from tenants.infrastructure.middlewares import get_user_id
from vocabulary.infrastructure.models.word import Word


class WordQuery:
    @staticmethod
    def list():
        return Word.objects.filter(user=get_user_id())
