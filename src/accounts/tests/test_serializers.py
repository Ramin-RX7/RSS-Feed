from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.serializers import UserRegisterSerializer,UserLoginSerializer



User = get_user_model()



class UserRegisterSerializerTest(TestCase):
    def test_passwords_match(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'testpassword',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_passwords_do_not_match(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'mismatchedpassword',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'password2': 'newpassword',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('newpassword'))

    def test_save_method(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'password2': 'newpassword',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password('newpassword'))



