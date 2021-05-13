from .base import *
import environ

env = environ.Env()

# reading .env file
environ.Env.read_env()

from .base_env import *
