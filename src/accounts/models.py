from django.db import models
from django.core.cache import caches
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from core.models import BaseModel
from .validators import username_validator
from .managers import UserManager



auth_cache = caches["auth"]




class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    username = models.CharField(
        unique=True,
        validators=[username_validator, MinLengthValidator(5),MaxLengthValidator(16)],
        max_length=16
    )
    email = models.EmailField(unique=True)

    objects = UserManager()

    first_name = models.CharField(blank=True, max_length=50)
    last_name =  models.CharField(blank=True, max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = "email"  # READMORE
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def logout(self, jti:str) -> bool:
        if auth_cache.get(f"{self.id}|{jti}"):
            auth_cache.delete(f"{self.id}|{jti}")
            return True
        return False



_login_types = models.TextChoices("login_type","login refresh access other register")
class UserTracking(BaseModel):
    user_id = models.IntegerField(editable=False,primary_key=True)
    last_login = models.DateTimeField()
    last_userlogin = models.DateTimeField()
    login_type = models.CharField(choices=_login_types.choices, max_length=10, default="register")
    user_agent = models.TextField()
    ip = models.CharField(max_length=75)
    # last_seen = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user_id} ({self.login_types})"
