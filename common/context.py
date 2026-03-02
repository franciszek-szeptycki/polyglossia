from contextvars import ContextVar
from typing import Optional

user_id_ctx: ContextVar[Optional[int]] = ContextVar("user_id", default=None)


class UserContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = user_id_ctx.set(
            request.user.id if request.user.is_authenticated else None
        )

        try:
            response = self.get_response(request)
        finally:
            user_id_ctx.reset(token)

        return response
