from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Timezone settings
TIME_ZONE = 'America/New_York'
USE_TZ = True
REDIS_URL = os.getenv('REDIS_URL')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

try:
    from .local import *
except ImportError:
    pass
