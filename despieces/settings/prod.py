import django_heroku
from .base import *
django_heroku.settings(locals())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'URL': os.getenv("DATABASE_URL"),
    }
}
