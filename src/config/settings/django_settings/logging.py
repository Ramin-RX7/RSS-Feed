from ..base import BASE_ENV


__all__ = ("LOGGING",)



LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "formatters": {
        'verbose': {
            'format': '[{levelname}] {asctime} | {message}',
            'style': '{',
        },
    },
    "handlers": {
        'celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    "loggers": {
        'celery-logger': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
