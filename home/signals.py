import requests

from django.conf import settings
from django.urls import reverse
from wagtail.core.signals import workflow_submitted, workflow_cancelled, workflow_approved, workflow_rejected


def post_message_to_slack(text, context):
    if not (settings.SLACK_NOTIFICATIONS_WEBHOOK and settings.SLACK_NOTIFICATIONS_CHANNEL):
        return

    payload = {
        'channel': settings.SLACK_NOTIFICATIONS_CHANNEL,
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': text,
                }
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'plain_text',
                        'text': context,
                        'emoji': True,
                    }
                ]
            }
        ],
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


def notify_submitted(sender, instance, user, **kwargs):
    message_format = """{environment}The page "{page_title}" has been submitted to the workflow "{workflow_name}"
<{page_url}|Edit page>
<{history_url}|Workflow history>
"""

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_cancelled(sender, instance, user, **kwargs):
    message_format = """{environment}The workflow "{workflow_name}" has been cancelled for page "{page_title}"
<{page_url}|Edit page>
<{history_url}|Workflow history>
"""

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_approved(sender, instance, user, **kwargs):
    message_format = """{environment}The page "{page_title}" has been approved in the workflow "{workflow_name}"
<{page_url}|Edit page>
<{history_url}|Workflow history>
"""

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_rejected(sender, instance, user, **kwargs):
    message_format = """{environment}The page "{page_title}" has been rejected in the workflow "{workflow_name}"
<{page_url}|Edit page>
<{history_url}|Workflow history>
"""

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def workflow_notify_slack(message_format, workflow_state, user):
    page = workflow_state.page
    page_url = settings.BASE_URL + reverse('wagtailadmin_pages:edit', args=(page.pk, ))
    workflow_history_url = settings.BASE_URL + reverse('wagtailadmin_pages:workflow_history_detail', args=(page.pk, workflow_state.pk))
    if 'staging' in settings.BASE_URL:
        environment = '[STAGING] '
    elif 'devel' in settings.BASE_URL:
        environment = '[DEVELOP] '
    elif 'localhost' in settings.BASE_URL:
        environment = '[LOCAL] '
    else:
        environment = ''

    text = message_format.format(
        page_title=workflow_state.page.get_admin_display_title(),
        workflow_name=workflow_state.workflow.name,
        page_url=page_url,
        history_url=workflow_history_url,
        environment=environment,
    )
    context = f'User: {user.first_name} {user.last_name}'
    post_message_to_slack(text, context)


workflow_submitted.connect(notify_submitted)
workflow_cancelled.connect(notify_cancelled)
workflow_approved.connect(notify_approved)
workflow_rejected.connect(notify_rejected)
