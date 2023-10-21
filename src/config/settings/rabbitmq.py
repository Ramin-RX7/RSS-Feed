import pika

from .base import BASE_ENV


__all__ = ("RABBIT_URL",)

RABBIT_URL = pika.URLParameters(BASE_ENV("RABBIT_URL"))
