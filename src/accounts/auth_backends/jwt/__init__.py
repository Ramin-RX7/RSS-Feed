import jwt

from django.core.cache import caches

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from accounts.models import User
from .utils import decode_jwt,generate_tokens


auth_cache = caches["auth"]



class JWTAuthBackend(BaseAuthentication):
    authentication_header_prefix = 'Token'
    authentication_header_name = 'Authorization'

    def authenticate_header(self, request):
        return self.authentication_header_prefix

    def authenticate(self, request):
        user_agent = self._get_user_agent(request.headers)

        token = self._get_access_token(request)

        payload = self._validate_access_token(token)

        user = self._get_user(payload)

        jti = payload.get('jti')
        self._validate_cache_data(user, jti, user_agent)

        print("ALL PASSES")
        return user, payload


    def _get_user_agent(self, headers):
        user_agent = headers.get("user-agent")
        if user_agent is None:
            raise exceptions.PermissionDenied('user-agent header is not provided')
        return user_agent

    def _get_access_token(self, request):
        auth_header = request.headers.get(self.authentication_header_name)
        if not auth_header:
            raise exceptions.PermissionDenied("No access token")
        prefix,token = auth_header.split(' ')
        if prefix != self.authentication_header_prefix:
            raise exceptions.PermissionDenied('Token prefix missing')
        return token

    def _validate_access_token(self, token):
        try:
            return decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAuthenticated('Access token expired') from None

    def _get_username(self, payload):
        username = payload.get('username')
        if username is None:
            raise exceptions.PermissionDenied('User identifier not found')
        return username

    def _get_user(self, payload):
        username = self._get_username(payload)
        user = User.objects.get(username=username)
        if not user.is_active:
            raise exceptions.PermissionDenied('User is inactive')
        return user

    def _validate_cache_data(self, user, jti, agent):
        user_redis_jti = auth_cache.get(f"{user.id}|{jti}")
        if user_redis_jti is None:
            raise exceptions.PermissionDenied(
                'No refresh token Found, please login again.')
        if user_redis_jti != agent:
            raise exceptions.PermissionDenied(
                'Invalid refresh token, please login again.')
