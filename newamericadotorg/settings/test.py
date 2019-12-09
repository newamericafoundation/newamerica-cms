from .base import *

SECRET_KEY = "TEST_KEY"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newamerica',
        'HOST': 'localhost',
    }
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'search.backend',
        'URLS': ["http://localhost:9200/"],
        'INDEX': 'test',
        'TIMEOUT': 1500,
    }
}
