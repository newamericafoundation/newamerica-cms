from .base import *


DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
