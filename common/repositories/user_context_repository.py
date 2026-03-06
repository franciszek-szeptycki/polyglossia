from common.context import user_id_ctx


class UserContextRepository:
    def _get_user_id(self) -> int:
        if user_id := user_id_ctx.get():
            return user_id
        raise ValueError("No user id in context")
