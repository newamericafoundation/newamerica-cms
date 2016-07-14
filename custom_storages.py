from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
    bucket_name = settings.STATIC_BUCKET_NAME

class MediaStorage(S3BotoStorage):
    bucket_name = settings.MEDIA_BUCKET_NAME
    file_overwrite = False
