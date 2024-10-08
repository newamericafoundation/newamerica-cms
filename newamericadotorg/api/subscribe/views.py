import json
from urllib.request import urlopen

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from subscribe.mailchimp import update_subscriber
from subscribe.models import MailingListSegment


@api_view(["POST"])
@permission_classes((AllowAny,))
def subscribe(request):
    params = request.query_params
    recaptcha_response = params.get("g-recaptcha-response", None)
    if not recaptcha_response:
        return Response({"status": "UNVERIFIED"})

    recaptcha_url = (
        "https://www.google.com/recaptcha/api/siteverify?response=%s&secret=%s"
        % (recaptcha_response, settings.RECAPTCHA_SECRET_KEY)
    )
    verification = urlopen(recaptcha_url).read()
    verification = json.loads(verification)

    if not verification["success"]:
        return Response({"status": "UNVERIFIED"})

    subscriptions = params.getlist("subscriptions[]", [])
    subscription_titles = list(MailingListSegment.objects.filter(
        pk__in=subscriptions,
    ).values_list('title', flat=True))

    zipcode = params.get("zipcode", None)
    custom_fields = {}

    if zipcode:
        custom_fields['ZIP'] = zipcode

    status = update_subscriber(params.get("email"), params.get("name"), subscription_titles, custom_fields)

    return Response({"status": status})
