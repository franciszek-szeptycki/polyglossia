from tenants.infrastructure.repositories import tenant_repository
from contextvars import ContextVar
from typing import Optional

user_id_ctx: ContextVar[Optional[int]] = ContextVar("user_id", default=None)

def get_user_id() -> int:
    if user_id := user_id_ctx.get():
        return user_id
    raise ValueError("No user id in context")


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.user.id if request.user.is_authenticated else None

        if not user_id:
            return self.get_response(request)

        token = user_id_ctx.set(user_id)
        try:
            request.tenant = tenant_repository.get_by_user_id(user_id=user_id)
            response = self.get_response(request)
        finally:
            user_id_ctx.reset(token)

        return response
