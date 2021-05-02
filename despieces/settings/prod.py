from .base import *

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {'default': env.db_url_config(engine='django.db.backends.postgresql_psycopg2'), }
}

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
