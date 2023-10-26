import jwt

from django.core.cache import caches
from django.utils.translation import gettext_lazy as _
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

        return user, payload


    def _get_user_agent(self, headers):
        user_agent = headers.get("user-agent")
        if user_agent is None:
            raise exceptions.PermissionDenied(_('user-agent header is not provided'))
        return user_agent

    def _get_access_token(self, request):
        auth_header = request.headers.get(self.authentication_header_name)
        if not auth_header:
            raise exceptions.PermissionDenied(_("No access token"))
        full_token = auth_header.split(' ')
        if (len(full_token) != 2) or (full_token[0] != self.authentication_header_prefix):
            raise exceptions.PermissionDenied(_('Token prefix missing'))
        return full_token[1]

    def _validate_access_token(self, token):
        try:
            return decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise exceptions.NotAuthenticated(_('Access token expired')) from None
        except jwt.DecodeError:
            raise exceptions.ParseError(_("invalid access token"))

    def _get_username(self, payload):
        username = payload.get('username')
        if username is None:
            raise exceptions.PermissionDenied(_('User identifier not found'))
        return username

    def _get_user(self, payload):
        username = self._get_username(payload)
        user = User.objects.get(username=username)
        if not user.is_active:
            raise exceptions.PermissionDenied(_('User is inactive'))
        return user

    def _validate_cache_data(self, user, jti, agent):
        user_redis_jti = auth_cache.get(f"{user.id}|{jti}")
        if user_redis_jti is None:
            raise exceptions.PermissionDenied(
                _('Not Found in cache, login again.'))
        if user_redis_jti != agent:
            raise exceptions.PermissionDenied(
                _('Invalid refresh token, please login again.'))




    def get_new_tokens(self, request):
        user_agent = self._get_user_agent(request.headers)

        refresh_token = self._get_refresh_token(request)
        payload = self._get_refresh_payload(refresh_token)

        user = self._get_user(payload)

        jti = payload.get('jti')
        self._validate_cache_data(user, jti, user_agent)

        self.deprecate_refresh_token(user, jti, user_agent)

        return generate_tokens(user.username)



    def _get_refresh_token(self, request):
        token = request.data.get("refresh_token")
        if token is None:
            raise exceptions.PermissionDenied(
                _('Authentication credentials were not provided.'))
        return token

    def _get_refresh_payload(self, token):
        try:
            return decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise exceptions.PermissionDenied(
                _('Expired refresh token, please login again.')) from None
        except jwt.DecodeError:
            raise exceptions.ParseError(_("invalid refresh token"))

    def deprecate_refresh_token(self, user, jti, user_agent):
        auth_cache.delete(f"{user.id}|{jti}")
