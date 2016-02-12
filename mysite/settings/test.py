from .base import *

SECRET_KEY = "TEST_KEY"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newamerica',
        'HOST': 'localhost',
    }
}
