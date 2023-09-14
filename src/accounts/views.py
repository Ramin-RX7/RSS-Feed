from django.core.cache import caches
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .auth_backends import LoginAuthBackend, JWTAuthBackend
from .auth_backends.jwt.utils import generate_tokens,decode_jwt,_save_cache,_get_user_agent
from .models import User


auth_cache = caches["auth"]





class UserRegisterView(CreateAPIView):
    """
    User Registration end point.

    Handles validation and creating a new user.

    Args:
        username (str): The desired username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.
        password2 (str): A confirmation of the password.

    Returns:
        dict: A dictionary containing user registration data.

    Response Schema:
    ```
        {
            "username": str,
            "email": str,
        }
    ```
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer


class UserLoginView(APIView):
    """
    User Login api end point.

    Serializer for user registration. Handles validation and creating a new user.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: A dictionary containing access and refresh token.

    Response Schema:
    ```
        {
            "access_token": str,
            "refresh_token": str,
        }
    ```
    """
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




class RefreshToken(APIView):
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            JWTAuthBackend().authenticate(request)
        except:
            pass
        else:
            return Response({"message":"already authenticated"})

        refresh_token = request.data.get('refresh_token')
        auth = JWTAuthBackend()
        jti,access_token,refresh_token = auth.get_new_tokens(request)

        payload = decode_jwt(refresh_token)
        _save_cache(auth._get_user(payload), jti, auth._get_user_agent(request.headers))
        # _save_cache(request.auth["username"], jti, request.headers["user-agent"])

        data = {
            "access": access_token,
            "refresh": refresh_token
        }
        return Response(data, status=status.HTTP_201_CREATED)



class LogoutView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            jti = request.auth.get("jti")
            user = User.objects.get(username=request.auth.get("username"))
            print(jti, user)
            auth_cache.delete(f"{user.id}|{jti}")
            return Response({"message": "Successful Logout"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": f"{type(e)}: {e}"}, status=status.HTTP_400_BAD_REQUEST)



class JWTAuthTestView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "hi"}, status=status.HTTP_205_RESET_CONTENT)

