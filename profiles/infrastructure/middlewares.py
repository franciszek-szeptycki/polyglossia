from profiles.consts import Language
from profiles.domain.entities import ProfileDTO
from profiles.infrastructure.repositories import profile_repository
from contextvars import ContextVar
from typing import List, Optional

profile_ctx: ContextVar[Optional[ProfileDTO]] = ContextVar("profile", default=None)

def get_profile_id() -> int:
    if profile := profile_ctx.get():
        return profile.id
    raise ValueError("No profile in the context")


class ProfileMiddleware:

    IGNORE_PATHS = ['/accounts', '/admin']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.IGNORE_PATHS):
            return self.get_response(request)

        user_id = request.user.id if request.user.is_authenticated else None

        if not user_id:
            return self.get_response(request)

        profile: ProfileDTO = profile_repository.get_active_profile(user_id=user_id)
        profiles: List[ProfileDTO] = profile_repository.get_all_for_user(user_id=user_id)

        context_token = profile_ctx.set(profile)

        request.profiles__profile = profile
        request.profiles__available_profiles = profiles
        print(f"ProfileMiddleware: profile={profile}, profiles={profiles}")

        try:
            response = self.get_response(request)
        finally:
            profile_ctx.reset(context_token)

        return response
