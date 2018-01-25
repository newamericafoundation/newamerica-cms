from .base import *

import os

# Timezone settings
TIME_ZONE = 'America/New_York'
USE_TZ = True


DEBUG = False

APPEND_SLASH = True

SECRET_KEY = os.getenv("SECRET_KEY")

#ADMINS = [('Kirk', 'jackson@newamerica.org'), ('Andrew', 'lomax@newamerica.org')]

# Will be changed to final host url
ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True

# s3 bucket settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# media file settings
MEDIA_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_MEDIA_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_BUCKET_NAME

MEDIA_URL = "https://%s/" % S3_MEDIA_DOMAIN
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# static file settings
STATIC_BUCKET_NAME = os.getenv('STATIC_S3_BUCKET_NAME')
S3_STATIC_DOMAIN = '%s.s3.amazonaws.com' % STATIC_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

STATICFILES_LOCATION='static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)

COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE

# Elastic Search setup
es_url = os.getenv('SEARCHBOX_URL', "http://localhost:9200/")

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch2',
        'URLS': [es_url],
        'INDEX': 'elasticsearch',
        'TIMEOUT': 1500,
    }
}

ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY')
}

# Email backend configuration
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
POSTMARK_SENDER = os.getenv("POSTMARK_SENDER")
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
SERVER_EMAIL = POSTMARK_SENDER
REDIS_URL = os.getenv('REDIS_URL')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

try:
    from .local import *
except ImportError:
    pass
