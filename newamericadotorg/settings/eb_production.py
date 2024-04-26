import os

from .base import *  # noqa: F403

# Timezone settings
TIME_ZONE = 'America/New_York'
USE_TZ = True


DEBUG = False

APPEND_SLASH = True

SECRET_KEY = os.getenv("SECRET_KEY")

# Will be changed to final host url
ALLOWED_HOSTS = [
    '.newamerica.org',
    # 'na-staging.herokuapp.com',
    # 'na-develop.herokuapp.com',
]

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_SECONDS = 63072000 # 2 years in seconds

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

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
    'ACL': 'public-read',
}
STATIC_BUCKET_NAME = os.getenv('STATIC_S3_BUCKET_NAME', None)

if STATIC_BUCKET_NAME is not None:
    # Use S3 for static
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    S3_STATIC_DOMAIN = '%s.s3.amazonaws.com' % STATIC_BUCKET_NAME
    CLOUDFRONT_STATIC_URL = os.getenv('STATIC_URL')
    #STATIC_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)
    STATIC_URL = "%s/%s/" % (CLOUDFRONT_STATIC_URL, STATICFILES_LOCATION)

    # COMPRESS_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)
    # COMPRESS_STORAGE = STATICFILES_STORAGE

else:
    # Serve static from the web server using Whitenoise
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_URL = '/static/'

    STATICFILES_LOCATION = ''
    S3_STATIC_DOMAIN = 'notusingthis.s3.amazonaws.com'
    CLOUDFRONT_STATIC_URL = ''


# Elastic Search setup
es_url = os.getenv('SEARCHBOX_URL', "http://localhost:9200/")

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'search.backend',
        'URLS': [es_url],
        'INDEX': 'elasticsearch',
        'TIMEOUT': 1500,
    }
}

ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY')
}

# Sentry

if 'SENTRY_DSN' in os.environ:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()],
        environment=os.environ['SENTRY_ENVIRONMENT'],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


# Email backend configuration
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
POSTMARK_SENDER = os.getenv("POSTMARK_SENDER")
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
SERVER_EMAIL = POSTMARK_SENDER
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False
REDIS_URL = os.getenv(
    'REDIS_TLS_URL',
    os.getenv('REDIS_URL'),
)

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
            'CONNECTION_POOL_KWARGS': {
                'ssl_cert_reqs': None,
            },
        },
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
    from .local import *  # noqa: F403
except ImportError:
    pass

# Wagtail settings

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = os.getenv('BASE_URL', None)

if WAGTAILADMIN_BASE_URL is None:
    WAGTAILADMIN_BASE_URL = 'https://www.newamerica.org'
