from profiles.infrastructure.repositories import profile_repository


class ChangeUserProfileService:

    def __init__(self, *, profile_repo):
        self.profile_repo = profile_repo

    def execute(self, *, user_id: int, profile_id: int):
        profiles = self.profile_repo.get_all_user_profiles(user_id=user_id)




change_user_profile_service = ChangeUserProfileService(profile_repo=profile_repository)
