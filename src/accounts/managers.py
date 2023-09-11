from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):

    def create_user(self, username, password, **other_fields):
        if username is None:
            raise ValueError("Username not given")

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **other_fields)
