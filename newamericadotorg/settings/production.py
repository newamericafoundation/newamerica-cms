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
ALLOWED_HOSTS = [
    '.newamerica.org',
    'na-staging.herokuapp.com'
]

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AWS_QUERYSTRING_AUTH = False
AWS_IS_GZIPPED = True

# s3 bucket settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# media file settings
AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')
CLOUDFRONT_ID = os.getenv('CLOUDFRONT_ID')
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

AWS_DEFAULT_ACL = "public-read"
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}
STATIC_BUCKET_NAME = os.getenv('STATIC_S3_BUCKET_NAME')
STATICFILES_LOCATION='static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
S3_STATIC_DOMAIN = '%s.s3.amazonaws.com' % STATIC_BUCKET_NAME
CLOUDFRONT_STATIC_URL = os.getenv('STATIC_URL')
#STATIC_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)
STATIC_URL = "%s/%s/" % (CLOUDFRONT_STATIC_URL, STATICFILES_LOCATION)

# COMPRESS_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)
# COMPRESS_STORAGE = STATICFILES_STORAGE

# Elastic Search setup
es_url = os.getenv('SEARCHBOX_URL', "http://localhost:9200/")

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch2',
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

WAGTAILFRONTENDCACHE = {
    'cloudfront': {
        'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudfrontBackend',
        'DISTRIBUTION_ID': 'E3IZZ8NUJMHTIF',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'newamericadotorg.api.pagination.CustomPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# PDF Generator
PDF_GENERATOR_URL = os.getenv('PDF_GENERATOR_URL')

try:
    from .local import *
except ImportError:
    pass
