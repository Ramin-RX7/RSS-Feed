from .base import BASE_ENV


CACHES = {
    "default": BASE_ENV.cache_url(backend="django_redis.cache.RedisCache"),
    "auth": {
        **BASE_ENV.cache_url("AUTH_CACHE", backend="django_redis.cache.RedisCache"),
        "timeout": 86400
    },
}
