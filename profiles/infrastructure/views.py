from django.http.response import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from profiles.domain.services.change_profile import change_user_profile_service


class ChangeProfileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        profile_id = request.POST.get('profile_id')

        change_user_profile_service.execute(user_id=int(request.user.id), profile_id=int(profile_id))

        return redirect(request.META.get('HTTP_REFERER', '/'))
