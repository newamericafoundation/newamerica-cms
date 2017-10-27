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
    'custom_contenttype',
    'issue',
    'weekly',
    'in_depth',
    'storages',
    'rss_feed',
    'subscribe',

    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.contrib.wagtailstyleguide',
    'wagtail.contrib.table_block',

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

    'rest_framework',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',

    'newamericadotorg.log_handlers.LogDNAMiddleware',
    # minify html
    'django.middleware.gzip.GZipMiddleware',
]

ROOT_URLCONF = 'newamericadotorg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
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
                'newamericadotorg.settings.context_processors.content_types'
            ]
        },
    },
]

WSGI_APPLICATION = 'newamericadotorg.wsgi.application'


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
# MEDIA_URL = '/media/'
MEDIA_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_MEDIA_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_BUCKET_NAME

if MEDIA_BUCKET_NAME == 'local':
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = "https://%s/" % S3_MEDIA_DOMAIN

# MEDIA_URL = "https://%s/" % '%s.s3.amazonaws.com' % os.getenv('S3_BUCKET_NAME')

# Wagtail settings

WAGTAIL_SITE_NAME = "newamericadotorg"

WAGTAILIMAGES_IMAGE_MODEL = 'home.CustomImage'

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'newamericadotorg.api.pagination.CustomPagination'
}
