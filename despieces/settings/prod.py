from .base import *
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT")
    }
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# False if not in os.environ
DEBUG = env('DEBUG')
