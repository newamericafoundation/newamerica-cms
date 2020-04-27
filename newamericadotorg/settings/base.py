"""
Django settings for newamericadotorg project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url
import os

SECRET_KEY = os.getenv("SECRET_KEY")

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    'corsheaders',
    'home',
    'search',
    'programs',
    'person',
    'book',
    'article',
    'blog',
    'event',
    'conference',
    'podcast',
    'report',
    'policy_paper',
    'press_release',
    'quoted',
    'issue',
    'weekly',
    'in_depth',
    'other_content',
    'storages',
    'rss_feed',
    'subscribe',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.table_block',
    'wagtail.contrib.frontend_cache',

    'modelcluster',
    'compressor',
    'taggit',
    'wand',
    'willow',
    'anymail',
    'createsend',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',
    'rest_framework'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    # Gzip/minify
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'newamericadotorg.urls'
HTML_MINIFY = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'generated-templates'),
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'newamericadotorg.settings.context_processors.debug',
                'newamericadotorg.settings.context_processors.program_data',
                'newamericadotorg.settings.context_processors.about_pages',
                'newamericadotorg.settings.context_processors.locations',
                'newamericadotorg.settings.context_processors.meta'
            ]
        },
    },
]

WSGI_APPLICATION = 'newamericadotorg.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if 'S3_BUCKET_NAME' in os.environ and os.environ['S3_BUCKET_NAME'] != 'local':
    MEDIA_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_MEDIA_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_BUCKET_NAME
    MEDIA_URL = "https://%s/" % S3_MEDIA_DOMAIN
else:
    MEDIA_URL = '/media/'


# Basic authentication settings
# These are settings to configure the third-party library:
# https://gitlab.com/tmkn/django-basic-auth-ip-whitelist
if os.getenv("BASIC_AUTH_ENABLED", "false").lower().strip() == "true":
    # Insert basic auth as a first middleware to be checked first, before
    # anything else.
    MIDDLEWARE.insert(0, "baipw.middleware.BasicAuthIPWhitelistMiddleware")

    # This is the credentials users will have to use to access the site.
    BASIC_AUTH_LOGIN = os.getenv("BASIC_AUTH_LOGIN", "newamerica")
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "")

    # This is the list of network IP addresses that are allowed in without
    # basic authentication check.
    BASIC_AUTH_WHITELISTED_IP_NETWORKS = os.getenv("BASIC_AUTH_WHITELISTED_IP_NETWORKS", "").split(",")

    # This is the list of hosts that website can be accessed without basic auth
    # check. This may be useful to e.g. white-list "llamasavers.com" but not
    # "llamasavers.production.torchbox.com".
    if "BASIC_AUTH_WHITELISTED_HTTP_HOSTS" in os.environ:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = os.getenv(
            "BASIC_AUTH_WHITELISTED_HTTP_HOSTS"
        ).split(",")


# Wagtail settings

WAGTAIL_SITE_NAME = "newamericadotorg"

WAGTAILIMAGES_IMAGE_MODEL = 'home.CustomImage'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                'bold',
                'italic',
                'pullquote',
                'na-blockquote',
                'h2',
                'h3',
                'h4',
                'h5',
                'ol',
                'ul',
                'hr',
                'embed',
                'link',
                'document-link',
                'image',
                'undo',
                'redo',
            ]
        }
    }
}

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'newamericadotorg.api.pagination.CustomPagination'
}
