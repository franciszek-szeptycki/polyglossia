from django.db import models

from profiles.consts import Language


class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="profiles")
    language = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in Language],
        default=Language.GERMAN.value
    )

    @staticmethod
    def create_default(*, user_id: int) -> 'Profile':
        profile = Profile(
            user_id=user_id,
            language=Language.GERMAN.value,
        )
        profile.save()
        return profile
