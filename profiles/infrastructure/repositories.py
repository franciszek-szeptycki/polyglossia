from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.models import Profile


class ProfileRepository:
    def get_by_user_id(self, user_id) -> ProfileDTO:
        profile = Profile.objects.get(pk=user_id)  # pyright: ignore[reportAttributeAccessIssue]
        return self._to_dto(profile)

    def _to_dto(self, profile: Profile) -> ProfileDTO:
        return ProfileDTO(
            id=profile.id,  # pyright: ignore[reportAttributeAccessIssue]
            user_id=profile.user_id,  # pyright: ignore[reportAttributeAccessIssue]
            language=profile.language,  # pyright: ignore[reportArgumentType]
        )

profile_repository = ProfileRepository()
