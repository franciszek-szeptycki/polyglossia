from typing import List
from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.repositories import ProfileRepository, profile_repository


class ChangeProfileService:
    def __init__(self, *, profile_repo: ProfileRepository):
        self.profile_repo = profile_repo

    def execute(self, *, user_id: int, profile_id: int):
        profiles: List[ProfileDTO] = self.profile_repo.get_all_user_profiles(user_id=user_id)

        for profile in profiles:
            if profile.id == profile_id:
                profile.is_active = True
            else:
                profile.is_active = False

        self.profile_repo.bulk_update(profiles=profiles)


change_user_profile_service = ChangeProfileService(profile_repo=profile_repository)
