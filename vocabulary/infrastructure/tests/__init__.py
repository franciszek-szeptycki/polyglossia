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
        data = {"title": "Tytuł z testu", "content": "Treść posta z testu"}

        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Word.objects.count(), 1)

        new_post = Word.objects.first()
        self.assertEqual(new_post.title, "Tytuł z testu")
        self.assertEqual(new_post.author, user)
