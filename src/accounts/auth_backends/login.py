from django.contrib.auth.backends import ModelBackend

from ..models import User



class LoginAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            user = user_qs.get()
            if user.check_password(password) and user.is_active:
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return
