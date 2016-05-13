from .base import *

import os

DEBUG = False

APPEND_SLASH = True

SECRET_KEY = os.getenv("SECRET_KEY")

# Will be changed to final host url
ALLOWED_HOSTS = ['*']

# s3 bucket settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

try:
    from .local import *
except ImportError:
    pass


# Elastic Search setup
es_url = os.getenv('SEARCHBOX_URL', "http://localhost:9200/")

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch',
        'URLS': [es_url],
        'INDEX': 'elasticsearch',
        'TIMEOUT': 1500,
        'AUTO_UPDATE': False,
    }
}


# Email backend configuration 
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = os.getenv("POSTMARK_API_KEY")
POSTMARK_SENDER = os.getenv("POSTMARK_SENDER")
POSTMARK_TEST_MODE   = False
POSTMARK_TRACK_OPENS = False
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
SERVER_EMAIL = POSTMARK_SENDER
