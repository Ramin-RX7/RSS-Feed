from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import User



class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_username_label(self):
        field_label = self.user._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_username_max_length(self):
        max_length = self.user._meta.get_field("username").max_length
        self.assertEqual(max_length, 16)

    def test_email_label(self):
        field_label = self.user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")

    def test_first_name_max_length(self):
        max_length = self.user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        max_length = self.user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_str_method(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_create_user(self):
        user = User.objects.create_user(
            username="newuser", email="new@example.com", password="newpassword"
        )
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertTrue(user.check_password("newpassword"))

    def test_create_user_invalid_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="0123456789012345",
                email="test@example.com",
                password="testpassword",
            )

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpassword"
        )
        self.assertEqual(admin_user.username, "admin")
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("adminpassword"))
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
