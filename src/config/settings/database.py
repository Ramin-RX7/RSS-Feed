from .base import BASE_ENV


DATABASES = {
    "default": BASE_ENV.db(),
}
