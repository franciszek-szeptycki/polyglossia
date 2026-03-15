from django.urls import path

from profiles.infrastructure.views import ChangeProfileView

urlpatterns = [
    path('change-profile/', ChangeProfileView.as_view(), name='change_profile'),
]
