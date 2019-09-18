import logging
import json

import boto3
from botocore.exceptions import ClientError
import requests

from django.conf import settings


def create_presigned_s3_upload_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name, object_name, ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return response


def render_pdf(html, filename):
    """
    Sends a request to the PDF generator to render the specified HTML and save the
    result to the given filename on S3.
    """
    response = requests.post(settings.PDF_GENERATOR_URL, json={
        'filename': filename,
        'base_url': 'https://www.newamerica.org/',
        'html': html,
        's3_upload': create_presigned_s3_upload_url(settings.AWS_STORAGE_BUCKET_NAME, filename),
    })

    return response.status_code == 200 and response.json()['s3_upload_response_status_code'] == 204
