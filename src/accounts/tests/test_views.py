from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User



class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_passwords_do_not_match(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword",
            "password2": "mismatchedpassword",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("login")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_with_valid_credentials(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(
            self.url, data, format="json", HTTP_USER_AGENT="sth"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(
            self.url, data, format="json", HTTP_USER_AGENT="sth"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid Credentials", str(response.data))


class RefreshTokenViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("token_refresh")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(
            reverse("login"), data, format="json", HTTP_USER_AGENT="sth"
        )
        self.refresh_token = response.data["refresh"]

    def test_refresh_token_with_valid_token(self):
        data = {"refresh_token": self.refresh_token}
        response = self.client.post(
            self.url, data, format="json", HTTP_USER_AGENT="sth"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token_with_invalid_token(self):
        invalid_token = "invalid-token"
        data = {"refresh_token": invalid_token}
        response = self.client.post(
            self.url, data, format="json", HTTP_USER_AGENT="sth"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def _test_refresh_token_without_authentication(self):
        response = self.client.post(self.url, format="json", HTTP_USER_AGENT="sth")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("logout")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(
            reverse("login"), data, format="json", HTTP_USER_AGENT="sth"
        )
        self.access_token = response.data["access"]

    def test_logout_with_valid_access_token(self):
        data = {"access_token": self.access_token}
        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_USER_AGENT="sth",
            HTTP_AUTHORIZATION=f"Token {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        # self.assertIsNone(auth_cache.get(f"{self.user.id}|{self.access_token['jti']}"))

    def test_logout_with_invalid_access_token(self):
        invalid_token = "invalid-token"
        data = {"access_token": invalid_token}
        response = self.client.post(
            self.url, data, format="json", HTTP_USER_AGENT="sth"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
