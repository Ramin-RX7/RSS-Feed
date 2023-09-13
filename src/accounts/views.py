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



auth_cache = caches["auth"]



class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = LoginAuthBackend().authenticate(request, username=username, password=password)
        if user is None:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jti,access_token,refresh_token = generate_tokens(username)
        user_agent = self._get_user_agent(request.headers)
        key = f"{user.id}|{jti}"
        value = f"{user_agent}"

        print(jti)
        auth_cache.set(key,value)
        # print(auth_cache.get(key))

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def _get_user_agent(self, headers):
        user_agent = headers.get("user-agent")
        if user_agent is None:
            raise exceptions.ValidationError('user-agent header is not provided')
        return user_agent


