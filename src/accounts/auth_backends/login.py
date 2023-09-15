from django.contrib.auth.backends import ModelBackend

from ..models import User



class LoginAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.get(username=username)
        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
