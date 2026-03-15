from django.contrib.auth.models import User
from django.db import models

from profiles.consts import Language


class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="profiles")
    language = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in Language],
        default=Language.GERMAN.value
    )
    is_selected = models.BooleanField(default=False)

    @staticmethod
    def create_missing_profiles_for_user(*, user_id: int):
        user = User.objects.get(id=user_id)

        existing_profiles = Profile.objects.filter(user=user)

        for language in Language:
            if not existing_profiles.filter(language=language.value).exists():
                profile = Profile(
                    user=user,
                    language=language.value,
                )
                print(f" --- Creating profile for language '{language.value}'")
                profile.save()

        default_profile = Profile.objects.filter(user=user)

        if 0 == default_profile.count():
            Profile.objects.get(user=user, language=Language.GERMAN.value).update(is_selected=True)
