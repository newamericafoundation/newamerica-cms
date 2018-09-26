from django.core.management.base import BaseCommand
from home.models import CustomImage
import boto3
import botocore
import os

s3 = boto3.resource('s3')
BUCKET_NAME = 'newamericadotorg'

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            os.mkdir('media/images')
        except:
            print('media/images exists')

        try:
            os.mkdir('media/original_images')
        except:
            print('media/original_images exists')


        images = CustomImage.objects.all().order_by('-created_at')

        for i in images:
            try:
                print('downloading ' + i.file.name + '...')
                s3.Bucket(BUCKET_NAME).download_file(i.file.name, 'media/' + i.file.name)

            except botocore.exceptions.ClientError as e:
                print('The object: ' + i.file.name + ' does not exist')

            for r in i.renditions.all():
                try:
                    print('downloading ' + r.file.name + '...')
                    s3.Bucket(BUCKET_NAME).download_file(r.file.name, 'media/' + r.file.name)
                except botocore.exceptions.ClientError as e:
                    print('The object: ' + r.file.name + ' does not exist')
