from .base import BASE_ENV


CACHES = {
    "default": BASE_ENV.cache(),
    "auth": BASE_ENV.cache_url("AUTH_CACHE"),
    # "default" : {
    #     "BACKEND":"django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379/0"
    # },
    # "auth" : {
    #     "BACKEND":"django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": "redis://127.0.0.1:6379/1",
    #     "TIMEOUT": 300
    # },
}