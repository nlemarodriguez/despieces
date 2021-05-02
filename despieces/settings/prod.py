from .base import *

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'URI': os.getenv("DATABASE_URL"),
    }
}

ALLOWED_HOSTS = ['despieces-dev.herokuapp.com']
