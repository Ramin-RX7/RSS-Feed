from django.core.cache import caches
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .auth_backends import LoginAuthBackend, JWTAuthBackend
from .auth_backends.jwt.utils import generate_tokens,decode_jwt,_save_cache,_get_user_agent



auth_cache = caches["auth"]





class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        user_agent = _get_user_agent(request.headers)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = LoginAuthBackend().authenticate(request, username=username, password=password)
        if user is None:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jti,access_token,refresh_token = generate_tokens(username)

        _save_cache(user, jti, user_agent)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(data, status=status.HTTP_201_CREATED)




class JWTAuthTestView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "hi"}, status=status.HTTP_205_RESET_CONTENT)

