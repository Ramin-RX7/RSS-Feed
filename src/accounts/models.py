from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator,MaxLengthValidator

from core.models import BaseModel
from .validators import username_validator
from .managers import UserManager




class User(AbstractBaseUser,PermissionsMixin,BaseModel):
    username = models.CharField(
        unique=True,
        validators=[username_validator, MinLengthValidator(5),MaxLengthValidator(16)],
        max_length=16
    )
    email = models.EmailField()

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

