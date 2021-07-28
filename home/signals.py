import requests

from django.conf import settings
from django.urls import reverse
from wagtail.core.signals import workflow_submitted


def post_message_to_slack(text, blocks=None):
    if not settings.SLACK_NOTIFICATIONS_WEBHOOK:
        return

    payload = {
        'channel': 'website-workflow-notifications',
        'blocks': [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': text,
            }
        }],
    }
    try:
        response = requests.post(
            settings.SLACK_NOTIFICATIONS_WEBHOOK,
            headers={'content-type': 'application/json'},
            json=payload,
        )
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response text: {response.text}')


def workflow_notify_slack(sender, instance, **kwargs):
    site = instance.page.get_site()
    url = site.root_url + reverse('wagtailadmin_pages:edit', args=(instance.page.pk, ))
    text = f'The page "{instance.page.title}" has been submitted to the workflow "{instance.workflow.name}".  Edit it at {url}'
    post_message_to_slack(text)


workflow_submitted.connect(workflow_notify_slack)
