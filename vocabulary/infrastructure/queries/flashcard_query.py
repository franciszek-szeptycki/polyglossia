from common.context import get_user_id
from vocabulary.infrastructure.models import Flashcard


class FlashcardQuery(GetUserId):
    @staticmethod
    def list(self):
        return Flashcard.objects.filter(user=get_user_id())
