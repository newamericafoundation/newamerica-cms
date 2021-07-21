import os

from .base import *


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = []

for template_engine in TEMPLATES:
    template_engine['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Timezone settings
TIME_ZONE = 'America/New_York'
USE_TZ = True
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'newamericadotorg.api.pagination.CustomPagination',
}

if 'ELASTICSEARCH_URL' in os.environ:
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'search.backend',
            'URLS': [os.environ['ELASTICSEARCH_URL']],
            'INDEX': 'elasticsearch',
            'TIMEOUT': 1500,
        }
    }

    TEST_ELASTICSEARCH = True

try:
    from .local import *
except ImportError:
    pass

# Wagtail settings

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://localhost:8000'