import environ
from .base import *

env = environ.Env()

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

from .base_env import *



