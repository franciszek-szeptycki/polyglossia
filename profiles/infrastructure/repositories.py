from typing import List
from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.models import Profile


class ProfileRepository:
    def get_by_user_id(self, *, user_id: int) -> ProfileDTO:
        profile = Profile.objects.get(pk=user_id)
        return self._to_dto(profile)

    def get_all_for_user(self, *, user_id: int) -> list[ProfileDTO]:
        profiles = Profile.objects.filter(user_id=user_id)
        return [self._to_dto(profile) for profile in profiles]

    def get_active_profile(self, *, user_id: int) -> ProfileDTO:
        profile = Profile.objects.filter(user_id=user_id, is_active=True).first()
        if profile:
            return self._to_dto(profile)
        raise Profile.DoesNotExist()

    def get_first_by_user_id(self, *, user_id: int) -> ProfileDTO:
        profile = Profile.objects.filter(user_id=user_id).first()
        if profile:
            return self._to_dto(profile)
        raise Profile.DoesNotExist()

    def get_all_user_profiles(self, *, user_id: int) -> list[ProfileDTO]:
        profiles = Profile.objects.filter(user_id=user_id)
        return [self._to_dto(profile) for profile in profiles]

    def bulk_update(self, *, profiles: List[ProfileDTO]):
        profile_models = [self._to_model(profile=profile) for profile in profiles]
        for model in profile_models:
            model.save()

    def _to_dto(self, profile: Profile) -> ProfileDTO:
        return ProfileDTO(
            id=profile.id,
            user_id=profile.user_id,
            language=profile.language,
            is_active=profile.is_active,
        )

    def _to_model(self, *, profile: ProfileDTO) -> Profile:
        return Profile(
            id=profile.id,
            user_id=profile.user_id,
            language=profile.language,
            is_active=profile.is_active,
        )

profile_repository = ProfileRepository()
