from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.repositories import profile_repository
from contextvars import ContextVar
from typing import Optional

profile_ctx: ContextVar[Optional[ProfileDTO]] = ContextVar("profile", default=None)

def get_profile_id() -> int:
    if profile := profile_ctx.get():
        return profile.id
    raise ValueError("No profile in the context")


class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.user.id if request.user.is_authenticated else None

        if not user_id:
            return self.get_response(request)

        # profile = profile_repository.get_all_for_user(user_id=user_id)
        profile: ProfileDTO = profile_repository.get_first_by_user_id(user_id=user_id)

        profile_token = profile_ctx.set(profile)

        request.profile = profile
        try:
            response = self.get_response(request)
        finally:
            profile_ctx.reset(profile_token)

        return response
