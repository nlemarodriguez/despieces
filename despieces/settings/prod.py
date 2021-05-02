import environ
from .base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}


