from .base import BASE_ENV


DATABASES = {
    'default': BASE_ENV.db(),
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'rssfeed',
    #     'USER': 'postgres',
    #     'PASSWORD': 'asdf1234',
    #     'HOST': 'postgres'
    # }
}