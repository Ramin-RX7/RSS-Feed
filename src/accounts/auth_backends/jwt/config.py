from datetime import datetime, timedelta

from django.conf import settings as SETTINGS


__all__ = ("SECRET_KEY", "ENCRYPTION", "ACCESS_TOKEN_EXPIRY", "REFRESH_TOKEN_EXPIRY")



SECRET_KEY = SETTINGS.SECRET_KEY
ENCRYPTION = "HS256"
_access_token_expiry = timedelta(seconds=60*60*24)  # one day in seconds
ACCESS_TOKEN_EXPIRY = datetime.utcnow() + _access_token_expiry
REFRESH_TOKEN_EXPIRY = datetime.utcnow() + _access_token_expiry*5
