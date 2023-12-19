import uuid
import logging

from django.core.cache import caches
from django.utils.translation import gettext_lazy as _
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action

from core.rabbitmq import RabbitMQ
from core.utils import get_nows
from podcasts.utils import get_user_recommendations
from interactions.models import Subscribe, Like
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
)
from .auth_backends import LoginAuthBackend, JWTAuthBackend
from .auth_backends.jwt.utils import (
    generate_tokens,
    decode_jwt,
    _save_cache,
    _get_user_agent,
    _get_remote_addr,
)
from .models import User
from .tasks import send_reset_password_email
from .permissions import IsOwner



auth_cache = caches["auth"]

logger = logging.getLogger("elastic")



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

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if (
            response.status_code == 201
        ):  # XXX: Should we only take accepted register calls?
            username = response.data["username"]
            user = User.objects.get(username=username)
            data = {
                "user_id": user.id,
                "timestamp": get_nows(),
                "message": "successful register",
                "action": "register",
                "user_agent": _get_user_agent(request.headers),
                "ip": _get_remote_addr(request.headers),
            }
            logger.info({
                **data,
                "event_type": "auth",
            })
            RabbitMQ.publish_s("auth", data)
        return response


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
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = LoginAuthBackend().authenticate(
            request, username=username, password=password
        )
        if user is None:  # ? should we save invalid login attempts?
            return Response(
                {"message": _("Invalid Credentials")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jti, access_token, refresh_token = generate_tokens(username)

        _save_cache(user, jti, user_agent)

        data = {
            "user_id": user.id,
            "timestamp": get_nows(),
            "message": "successful login",
            "action": "login",
            "user_agent": user_agent,
            "ip": _get_remote_addr(request.headers),
        }
        logger.info({
            **data,
            "event_type": "auth",
        })
        RabbitMQ.publish_s("auth", data)

        data = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    Recreate the refresh and access tokens.

    Only accepts requests containing the refresh token in the request data

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

    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            JWTAuthBackend().authenticate(request)
        except:
            pass
        else:
            return Response({"message": _("already authenticated")})

        auth = JWTAuthBackend()
        jti, access_token, refresh_token = auth.get_new_tokens(request)

        payload = decode_jwt(refresh_token)
        user = auth._get_user(payload)
        _save_cache(user, jti, auth._get_user_agent(request.headers))
        request.user = user

        elastic_data = {
            "user_id": user.id,
            "timestamp": get_nows(),
            "message": "successful login with refresh token",
            "action": "refresh",
            "user_agent": _get_user_agent(request.headers),
            "ip": _get_remote_addr(request.headers),
        }
        logger.info({
                **elastic_data,
                "event_type": "auth",
        })
        RabbitMQ.publish_s("auth", elastic_data)

        data = {"access": access_token, "refresh": refresh_token}
        return Response(data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """
    Logout api end-point.

    Only accepts requests containing the access token in the request data

    Response Schema:
    ```
        {}
    ```
    """

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            jti = request.auth.get("jti")
            user = User.objects.get(username=request.auth.get("username"))
            user.logout(jti)

            data = {
                "user_id": user.id,
                "timestamp": get_nows(),
                "message": "successful logout",
                "action": "logout",
                "user_agent": _get_user_agent(request.headers),
                "ip": _get_remote_addr(request.headers),
            }
            logger.info({
                **data,
                "event_type": "auth",
            })
            RabbitMQ.publish_s("auth", data)

            return Response({}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(
                {"message": _(f"{type(e)}: {e}")}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePassword(APIView):
    """
    Returns HTTP 202 code for successfull calls and HTTP 406 for invalid calls
    """

    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user: User = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not user.check_password(data["old_password"]):
            return Response(
                {"detail": _("invalid password")}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        if user.check_password(data["new_password"]):
            return Response(
                {"detail": _("new password can not be same as old password")},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        user.set_password(data["new_password"])
        user.save()

        data = {
            "user_id": user.id,
            "timestamp": get_nows(),
            "message": "successful password change",
            "action": "change-password",
            "user_agent": _get_user_agent(request.headers),
            "ip": _get_remote_addr(request.headers),
        }
        logger.info({
            **data,
            "event_type": "auth",
        })
        RabbitMQ.publish_s("auth", data)

        return Response(
            {"detail": _("password changed successfully")},
            status=status.HTTP_202_ACCEPTED,
        )


class ResetPassword(viewsets.ViewSet):
    def get(self, request, code):
        if user := auth_cache.get(f"reset_password_{code}"):
            return Response({"code": code}, status=status.HTTP_202_ACCEPTED)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, code):
        if self.get(request, code).status_code == 202:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_id = auth_cache.get(f"reset_password_{code}")
            user = User.objects.get(
                id=user_id
            )  # BUG: error when user delete the account in middle of resetting password process
            user.set_password(serializer.data["new_password"])
            user.save()
            auth_cache.delete(f"reset_password_{code}")
            data = {
                "user_id": user.id,
                "timestamp": get_nows(),
                "message": "successful reset-password",
                "action": "reset=password-request",
                "user_agent": _get_user_agent(request.headers),
                "ip": _get_remote_addr(request.headers),
            }
            logger.info({
                **data,
                "event_type": "auth",
            })
            RabbitMQ.publish_s("auth", data)
            return Response({}, status=status.HTTP_202_ACCEPTED)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=["POST"])
    def reset_password_request(self, request):
        email = request.POST.get("email")
        if not email:
            return Response(
                {"detail": _("email field not provided")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.get()
            code = str(uuid.uuid4())
            auth_cache.set(f"reset_password_{code}", user.id, timeout=60*15)
            send_reset_password_email.delay(user.email, code)
            data = {
                "user_id": user.id,
                "timestamp": get_nows(),
                "message": f"successful password reset request. sent email to {user.email}",
                "action": "password-reset-request",
                "user_agent": _get_user_agent(request.headers),
                "ip": _get_remote_addr(request.headers),
            }
            logger.info({
                **data,
                "event_type": "auth",
            })
            RabbitMQ.publish_s("auth", data)
        return Response({"send": _("ok")}, status=status.HTTP_200_OK)


class ProfileView(viewsets.ViewSet, RetrieveUpdateAPIView):
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"
    serializer_class = UserRegisterSerializer

    @action(detail=False)
    def subscriptions(self, request, *args, **kwargs):
        query_results = (
            Subscribe.objects.filter(user=self.get_object())
            .values("rss__id", "notification")
            .prefetch_related("rss")
        )
        result_list = [
            {"id": item["rss__id"], "notification": item["notification"]}
            for item in query_results
        ]
        return Response(result_list, status.HTTP_200_OK)

    @action(detail=False)
    def likes(self, request, *args, **kwargs):
        qs = Like.objects.filter(user=self.get_object()).values_list(
            "episode", flat=True
        )
        return Response(qs, status.HTTP_200_OK)

    @action(detail=False)
    def recommendations(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(get_user_recommendations(user), status.HTTP_200_OK)


class ActiveSessionsView(viewsets.ViewSet):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(user.active_sessions)

    def logout(self, request, session_code, *args, **kwargs):
        request.user.logout(session_code)
        return Response({}, status.HTTP_202_ACCEPTED)

    def logout_others(self, request, *args, **kwargs):
        current_jti = request.auth.get("jti")
        user = request.user
        for session in auth_cache.keys(f"{user.id}|*"):
            if session == f"{user.id}|{current_jti}":
                continue
            auth_cache.delete(session)
        return Response({}, status.HTTP_202_ACCEPTED)

    def logout_all(self, request, *args, **kwargs):
        user = request.user
        for session in user.active_sessions.keys():
            user.logout(session)
        return Response({}, status.HTTP_202_ACCEPTED)
