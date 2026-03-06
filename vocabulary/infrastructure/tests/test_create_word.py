from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from vocabulary.infrastructure.models import Word


class AddWordTestCase(TestCase):
    def test_create_post_authenticated(self):
        username = "testowy_user"
        password = "haslo123_secure"

        user = User.objects.create_user(username=username, password=password)

        login_successful = self.client.login(username=username, password=password)
        self.assertTrue(login_successful)

        url = reverse("word_create")
        data = {"text": "lorem", "context": "ipsum"}

        self.client.post(url, data)

        new_word = Word.objects.first()
        self.assertEqual(new_word.text, "lorem")
        self.assertEqual(new_word.context, "ipsum")
        self.assertEqual(new_word.user, user)
