from django.urls import path

from vocabulary.infrastructure.views.word import (
    WordCreateView,
    WordDeleteView,
    WordDetailView,
    WordListView,
    WordUpdateView,
)

urlpatterns = [
    path("", WordListView.as_view(), name="word_list"),
    path("add/", WordCreateView.as_view(), name="word_create"),
    path("<uuid:pk>/", WordDetailView.as_view(), name="word_detail"),
    path("<uuid:pk>/edit/", WordUpdateView.as_view(), name="word_edit"),
    path("<uuid:pk>/delete/", WordDeleteView.as_view(), name="word_delete"),
]
