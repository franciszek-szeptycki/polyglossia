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
    is_active = models.BooleanField(default=False)

    @staticmethod
    def seed_profiles_for_user(*, user_id: int):
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

        user_profiles = Profile.objects.filter(user_id=user.id, is_active=True)

        active_profiles = user_profiles.count()
        if active_profiles == 0:
            first = Profile.objects.filter(user_id=user.id).first()
            if first:
                first.is_active=True
                first.save()
            print(f"- Activated first profile for user '{user}'")
        elif active_profiles > 1:
            for profile in user_profiles:
                profile.update(is_active=False)
            first = Profile.objects.filter(user_id=user.id).first()
            if first:
                first.is_active=True
                first.save()
            print(f"- Activated first profile for user '{user}'")
