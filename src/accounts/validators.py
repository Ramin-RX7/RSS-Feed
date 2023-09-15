from django.core.exceptions import ValidationError
import re



def username_validator(username):
    if not re.fullmatch(r'\w+', username):
        raise ValidationError(
            'Username can only contain letters, numbers, and underscores.',
            code='invalid_username'
        )
    if not re.fullmatch(r'[a-zA-Z]\w+[a-zA-Z0-9]', username):
        raise ValidationError(
            'Username can only start with letters and end with letters or numbers',
            code='invalid_username'
        )
