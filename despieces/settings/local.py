from .base import *
import environ

env = environ.Env()

# reading .env file
environ.Env.read_env()
ALLOWED_HOSTS = ['*']

from .base_env import *
