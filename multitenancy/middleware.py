# multitenancy/middleware.py
from .thread_local import set_current_user


class MultitenancyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allauth ustawia request.user. Jeśli jest zalogowany, zapisujemy go.
        if request.user.is_authenticated:
            set_current_user(request.user)
        else:
            set_current_user(None)

        response = self.get_response(request)

        # Czyścimy po zakończeniu requestu
        set_current_user(None)
        return response
