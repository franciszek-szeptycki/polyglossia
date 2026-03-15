from profiles.infrastructure.middlewares import get_profile_id
from vocabulary.infrastructure.models import Flashcard


class FlashcardQuery:
    @staticmethod
    def active():
        return Flashcard.objects.filter(profile=get_profile_id(), is_active=True)
