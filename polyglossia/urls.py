from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # path("sentences/", include("sentences.urls")),
    path("accounts/", include("allauth.urls")),
    path("vocabulary/", include("vocabulary.urls")),
    path("", RedirectView.as_view(url="vocabulary/", permanent=False)),
]
