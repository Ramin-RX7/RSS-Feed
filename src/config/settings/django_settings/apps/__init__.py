INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "debug_toolbar",
    'drf_spectacular',
    'django_celery_beat',

    "core",
    "accounts",
    "interactions",
    "podcasts",
]

from .debug_toolbar import *
from .drf_spectacular import *
from .rest_framework import *
from .celery import *
