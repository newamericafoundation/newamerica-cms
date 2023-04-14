import requests

from django.conf import settings
from django.urls import reverse
from wagtail.models import PageLogEntry
from wagtail.signals import workflow_submitted, workflow_cancelled, workflow_approved, workflow_rejected, page_published


def get_environment_prefix():
    if 'staging' in settings.WAGTAILADMIN_BASE_URL:
        environment = '[STAGING] '
    elif 'devel' in settings.WAGTAILADMIN_BASE_URL:
        environment = '[DEVELOP] '
    elif 'localhost' in settings.WAGTAILADMIN_BASE_URL:
        environment = '[LOCAL] '
    else:
        environment = ''
    return environment


def post_message_to_slack(blocks):
    if not (settings.SLACK_NOTIFICATIONS_WEBHOOK and settings.SLACK_NOTIFICATIONS_CHANNEL):
        return

    payload = {
        'channel': settings.SLACK_NOTIFICATIONS_CHANNEL,
        'blocks': blocks,
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
    header_format = ':inbox_tray: Submission to {workflow_name}'
    message_format = '*<{preview_url}|{page_title}>* ({page_type}) submitted by {user_name}'

    workflow_notify_slack(
        header_format=header_format,
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


def workflow_notify_slack(message_format, workflow_state, user, header_format=None):
    blocks = []
    environment = get_environment_prefix()
    page = workflow_state.page
    if getattr(page.specific, 'parent_programs', None):
        program = f'{page.specific.parent_programs.first().title} '
    else:
        program = ''
    page_type = page.specific._meta.verbose_name.title()
    preview_url = settings.WAGTAILADMIN_BASE_URL + reverse('wagtailadmin_pages:workflow_preview', args=(page.pk, workflow_state.current_task_state.task.pk))
    edit_url = settings.WAGTAILADMIN_BASE_URL + reverse('wagtailadmin_pages:edit', args=(page.pk, ))
    workflow_history_url = settings.WAGTAILADMIN_BASE_URL + reverse('wagtailadmin_pages:workflow_history_detail', args=(page.pk, workflow_state.pk))
    workflow_name = workflow_state.workflow.name
    task_comment = workflow_state.current_task_state.comment
    if task_comment:
        comment = f' with comment \n>{task_comment}'
    else:
        comment = ''

    if header_format:
        header = header_format.format(
            workflow_name=workflow_name
        )
        header_block = {
            'type': 'header',
            'text': {
                'type': 'plain_text',
                'text': header,
            }
        }
        blocks.append(header_block)

    message_format = f'{environment}{message_format}'
    text = message_format.format(
        page_title=page.get_admin_display_title(),
        page_type=f'{program}{page_type}',
        page_url=page.full_url,
        preview_url=preview_url,
        comment=comment,
        user_name=f'{user.first_name} {user.last_name}',
    )

    blocks += [
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
                    'text': f'{workflow_name} | <{edit_url}|Edit page> | <{workflow_history_url}|Workflow history>',
                }
            ]
        },
    ]


    post_message_to_slack(blocks)


workflow_submitted.connect(notify_submitted)
workflow_cancelled.connect(notify_cancelled)
workflow_approved.connect(notify_approved)
workflow_rejected.connect(notify_rejected)


def publication_notify_slack(sender, instance, revision, **kwargs):
    environment = get_environment_prefix()
    page = instance
    parent_programs = getattr(page.specific, 'parent_programs', None)
    if parent_programs and parent_programs.first():
        program = f'{parent_programs.first().title} '
    else:
        program = ''
    page_type = f'{program}{page.specific._meta.verbose_name.title()}'
    user_name = f'{revision.user.first_name} {revision.user.last_name}'

    latest_log_entry = PageLogEntry.objects.filter(page=page).order_by('-timestamp').first()

    # If this was not published via workflow approval (so that we don't send a duplicate notification)
    if latest_log_entry and latest_log_entry.action != 'wagtail.workflow.approve':
        # If this is the first time the page is being published
        if page.first_published_at == page.last_published_at:
            message = f'{environment}*<{page.full_url}|{page.title}>* ({page_type}) published for the first time by {user_name}'
        else:
            message = f'{environment}*<{page.full_url}|{page.title}>* ({page_type}) published by {user_name}'
        blocks = [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': message,
                }
            },
        ]
        post_message_to_slack(blocks)

page_published.connect(publication_notify_slack)
