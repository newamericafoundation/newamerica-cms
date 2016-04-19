from .base import *

import os

DEBUG = True

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
