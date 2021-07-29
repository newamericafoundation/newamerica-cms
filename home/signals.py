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
                        'type': 'mrkdwn',
                        'text': context,
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
    message_format = ':exclamation::inbox_tray: *<{preview_url}|{page_title}>* ({page_type}) submitted by {user_name}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_cancelled(sender, instance, user, **kwargs):
    message_format = ':heavy_multiplication_x: *{page_title}* ({page_type}) cancelled by {user_name}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_approved(sender, instance, user, **kwargs):
    message_format = ':white_check_mark: *<{page_url}|{page_title}>* ({page_type}) approved by {user_name}{comment}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def notify_rejected(sender, instance, user, **kwargs):
    message_format = ':x: *{page_title}* ({page_type}) rejected by {user_name}{comment}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


def workflow_notify_slack(message_format, workflow_state, user):
    page = workflow_state.page
    page_type=f'{page.specific.parent_programs.first().title} {page.specific._meta.verbose_name.title()}'
    preview_url = settings.BASE_URL + reverse('wagtailadmin_pages:workflow_preview', args=(page.pk, workflow_state.current_task_state.task.pk))
    edit_url = settings.BASE_URL + reverse('wagtailadmin_pages:edit', args=(page.pk, ))
    workflow_history_url = settings.BASE_URL + reverse('wagtailadmin_pages:workflow_history_detail', args=(page.pk, workflow_state.pk))
    task_comment = workflow_state.current_task_state.comment
    if task_comment:
        comment = f' with comment \n>{task_comment}'
    else:
        comment = ''
    if 'staging' in settings.BASE_URL:
        environment = '[STAGING] '
    elif 'devel' in settings.BASE_URL:
        environment = '[DEVELOP] '
    elif 'localhost' in settings.BASE_URL:
        environment = '[LOCAL] '
    else:
        environment = ''

    message_format = f'{environment}{message_format}'
    text = message_format.format(
        page_title=page.get_admin_display_title(),
        page_type=page_type,
        page_url=page.full_url,
        preview_url=preview_url,
        comment=comment,
        user_name=f'{user.first_name} {user.last_name}',
    )
    context = f'{workflow_state.workflow.name} | <{edit_url}|Edit page> | <{workflow_history_url}|Workflow history>'
    post_message_to_slack(text, context)


workflow_submitted.connect(notify_submitted)
workflow_cancelled.connect(notify_cancelled)
workflow_approved.connect(notify_approved)
workflow_rejected.connect(notify_rejected)
