from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.infrastructure.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_model = get_user_model()
        users = user_model.objects.all()
        for user in users:
            print(f"Analyzing user '{user}'...")
            if 0 == user.profiles.all().count():
                Profile.create_missing_profiles_for_user(user_id=user.id)
                print(f"- Created missing profiles for user '{user}'")
