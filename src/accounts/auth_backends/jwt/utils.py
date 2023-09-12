import datetime
from uuid import uuid4

import jwt

from .config import *


def _generate_payload(username):
    return {
        'user_identifier': username,
        'iat': datetime.datetime.utcnow(),
        'jti': uuid4().hex,
    }

def _generate_refresh_token(base_payload):
    return {
        "token_type":"access",
        "exp":REFRESH_TOKEN_EXPIRY,
        **base_payload
    }

def _generate_access_token(base_payload):
    return {
        "token_type":"access",
        "exp":ACCESS_TOKEN_EXPIRY,
        **base_payload
    }



def generate_tokens(username):
    base_payload = _generate_payload(username)
    access_payload = _generate_access_token(base_payload)
    refresh_payload = _generate_refresh_token(base_payload)
    return (encode_payload(access_payload), encode_payload(refresh_payload))


