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

