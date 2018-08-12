import json
import os
from urllib.request import urlopen
from rest_framework.response import Response
from rest_framework.decorators import api_view

from subscribe.campaign_monitor import update_subscriber

@api_view(['POST'])
def subscribe(request):
    params = request.query_params
    recaptcha_response = params.get('g-recaptcha-response', None)
    if not recaptcha_response:
        return Response({
            'status': 'UNVERIFIED'
        });

    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify?response=%s&secret=%s' % (recaptcha_response, RECAPTCHA_SECRET_KEY)
    verification = urlopen(recaptcha_url).read()
    verification = json.loads(verification)

    if not verification['success']:
        return Response({
            'status': 'UNVERIFIED'
        });

    subscriptions = params.getlist('subscriptions[]', None)
    job_title = params.get('job_title', None)
    org = params.get('organization', None)
    zipcode = params.get('zipcode', None)
    custom_fields = []

    if job_title:
        custom_fields.append({ 'key': 'JobTitle', 'value': job_title })
    if org:
        custom_fields.append({ 'key': 'Organization', 'value': org })
    if zipcode:
        custom_fields.append({ 'key': 'MailingZip/PostalCode', 'value': zipcode })
    if subscriptions:
        for s in subscriptions:
            custom_fields.append({ 'key': 'Subscriptions', 'value': s })

    status = update_subscriber(params.get('email'), params.get('name'), custom_fields)

    return Response({
        'status': status
    });
