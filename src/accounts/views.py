from django.core.cache import caches
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import exceptions

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .auth_backends import LoginAuthBackend, JWTAuthBackend
from .auth_backends.jwt.utils import generate_tokens, decode_jwt
from .models import User





class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


