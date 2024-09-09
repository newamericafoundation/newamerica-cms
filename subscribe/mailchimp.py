import traceback
import urllib.parse
import requests
import hashlib
from enum import Enum
from django.conf import settings
from urllib.parse import urljoin
import logging
from subscribe.models import MailingListSegment

logger = logging.getLogger(__name__)


class StatusEnum(Enum):
    OK = "OK"
    BAD_REQUEST = "BAD_REQUEST"


class MailchimpError(Exception):
    pass


class MailchimpClient:
    def __init__(self, *, host, api_key):
        self.api_key = api_key
        self.host = host

    def _build_url(self, path):
        return urljoin(f"https://{self.host}", path)

    def _do_request(self, method, path, **kwargs):
        try:
            response = requests.request(
                method,
                self._build_url(path),
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise MailchimpError(f"Request to Mailchimp failed") from e

    def get(self, path):
        return self._do_request("GET", path)

    def post(self, path, data):
        return self._do_request("POST", path, json=data)

    def put(self, path, data):
        return self._do_request("PUT", path, json=data)

    def _get_subscriber_hash(self, email):
        return hashlib.md5(email.lower().strip().encode()).hexdigest()

    def get_tags(self, list_id):
        tags = []
        offset = 0
        count = 100

        while True:
            response = self.get(
                f"/3.0/lists/{list_id}/tag-search?count={count}&offset={offset}"
            )
            tags.extend(response["tags"])

            total_items = response["total_items"]
            if offset + count >= total_items:
                break

            offset += count

        return tags

    def subscribe(self, *, list_id, email, name, merge_fields, tags):
        subscriber_hash = self._get_subscriber_hash(email)
        return self.put(
            f"/3.0/lists/{list_id}/members/{subscriber_hash}",
            {
                "email_address": email,
                "status": "pending",
                "merge_fields": merge_fields,
                "tags": tags,
            },
        )

    def get_subscriber(self, *, list_id, email):
        return self.get(f"/3.0/lists/{list_id}/members/{email}")


def _get_client():
    host = settings.MAILCHIMP_HOST
    api_key = settings.MAILCHIMP_API_KEY

    if not host:
        raise ValueError(
            "MAILCHIMP_HOST is not set. Set this to the base API host for your Mailchimp account, for example: us22.api.mailchimp.com"
        )
    if not api_key:
        raise ValueError("MAILCHIMP_API_KEY is not set. Set this to your Mailchimp API key.")

    return MailchimpClient(host=host, api_key=api_key)


def update_segments():
    client = _get_client()
    list_id = settings.MAILCHIMP_LIST_ID

    tags = client.get_tags(list_id)
    existing_tag_names = set(MailingListSegment.objects.values_list("title", flat=True))

    # Process tags and create/update MailingListSegment objects
    current_tag_names = set()
    for tag in tags:
        tag_name = tag["name"]
        current_tag_names.add(tag_name)

        MailingListSegment.objects.update_or_create(
            title=tag_name,
        )

    # Delete MailingListSegment objects for tags that no longer exist
    tags_to_delete = existing_tag_names - current_tag_names
    MailingListSegment.objects.filter(title__in=tags_to_delete).delete()

    return len(current_tag_names)


def update_subscriber(email, name, tags, custom_fields):
    client = _get_client()
    try:
        client.subscribe(
            list_id=settings.MAILCHIMP_LIST_ID,
            email=email,
            name=name,
            merge_fields=custom_fields,
            tags=tags,
        )
        return StatusEnum.OK.value
    except MailchimpError:
        logger.warning("Failed to create subscriber in Mailchimp", exc_info=True)
        return StatusEnum.BAD_REQUEST.value
