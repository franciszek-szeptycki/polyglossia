from django.urls import path

from sentences.infrastructure.views.sentence import ContactView

urlpatterns = [
    path("", ContactView.as_view(), name="sentence"),
]
