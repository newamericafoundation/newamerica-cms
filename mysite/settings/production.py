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

STATICFILES_LOCATION='static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (S3_STATIC_DOMAIN, STATICFILES_LOCATION)


# Elastic Search setup
es_url = os.getenv('SEARCHBOX_URL', "http://localhost:9200/")

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch',
        'URLS': [es_url],
        'INDEX': 'elasticsearch',
        'TIMEOUT': 1500,
    }
}

ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": 'newamerica.org',
    "MAILGUN_DOMAIN": os.getenv('MAILGUN_DOMAIN'),
    "MAILGUN_PUBLIC_KEY": os.getenv('MAILGUN_PUBLIC_KEY'),
    "MAILGUN_SMTP_LOGIN": os.getenv('MAILGUN_SMTP_LOGIN'),
    "MAILGUN_SMTP_PASSWORD": os.getenv('MAILGUN_API_KEY'),
    "MAILGUN_SMTP_PORT": os.getenv('MAILGUN_SMTP_PORT'),
    "MAILGUN_SMTP_SERVER": os.getenv('MAILGUN_SMTP_SERVER'),
}

# Email backend configuration
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
POSTMARK_SENDER = os.getenv("POSTMARK_SENDER")
DEFAULT_FROM_EMAIL = POSTMARK_SENDER
SERVER_EMAIL = POSTMARK_SENDER

try:
    from .local import *
except ImportError:
    pass
