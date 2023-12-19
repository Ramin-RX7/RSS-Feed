from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from .auth_backends import JWTAuthBackend



def auth_action(func):
    def wrapper(self, request, *args, **kwargs):
        if not (auth := JWTAuthBackend().authenticate(request)):
            return Response(
                {"details": _("login required")}, status=status.HTTP_403_FORBIDDEN
            )
        request.user = auth[0]
        request.payload = auth[1]
        return func(self, request, *args, **kwargs)

    return wrapper
