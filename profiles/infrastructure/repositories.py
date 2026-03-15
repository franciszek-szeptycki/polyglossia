from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.models import Profile


class ProfileRepository:
    def get_by_user_id(self, *, user_id: int) -> ProfileDTO:
        profile = Profile.objects.get(pk=user_id)
        return self._to_dto(profile)

    def get_all_for_user(self, *, user_id: int) -> list[ProfileDTO]:
        profiles = Profile.objects.filter(user_id=user_id)
        return [self._to_dto(profile) for profile in profiles]

    def get_first_by_user_id(self, *, user_id: int) -> ProfileDTO:
        profile = Profile.objects.filter(user_id=user_id).first()
        if profile:
            return self._to_dto(profile)
        raise Profile.DoesNotExist()

    def _to_dto(self, profile: Profile) -> ProfileDTO:
        return ProfileDTO(
            id=profile.id,
            user_id=profile.user_id,
            language=profile.language,
        )

profile_repository = ProfileRepository()
