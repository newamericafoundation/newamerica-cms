import requests

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from wagtail.core.models import PageLogEntry, BaseViewRestriction
from wagtail.core.signals import workflow_submitted, workflow_cancelled, workflow_approved, workflow_rejected, page_published


def get_environment_prefix():
    if 'staging' in settings.BASE_URL:
        environment = '[STAGING] '
    elif 'devel' in settings.BASE_URL:
        environment = '[DEVELOP] '
    elif 'localhost' in settings.BASE_URL:
        environment = '[LOCAL] '
    else:
        environment = ''
    return environment


def get_restrictions_text(page):
    restrictions = page.get_view_restrictions()

    if not restrictions.first():
        return ''

    restriction = restrictions.first()
    restriction_type = restriction.restriction_type
    restrictions_text = f' with restriction {restriction.get_restriction_type_display()}'

    if restriction_type == BaseViewRestriction.PASSWORD and restriction.password:
        restrictions_text += f': `{restriction.password}`'
    elif restriction_type == BaseViewRestriction.GROUPS and restriction.groups.exists():
        groups_list = list(restriction.groups.all())
        restrictions_text += f': {groups_list[0]}'
        for group in groups_list[1:]:
            restrictions_text += f', {group}'
    return restrictions_text


def get_page_text(page):
    parent_programs = getattr(page.specific, 'parent_programs', None)
    if parent_programs and parent_programs.first():
        program = f'{parent_programs.first().title} '
    else:
        program = ''
    page_type = f'{program}{page.specific._meta.verbose_name.title()}'

    return f'<{page.full_url}|{page.title}>* ({page_type})'


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


@receiver(workflow_submitted)
def notify_submitted(sender, instance, user, **kwargs):
    header_format = ':inbox_tray: Submission to {workflow_name}'
    message_format = '*<{preview_url}|{page_title}>* ({page_type}) submitted by {user_name}'

    workflow_notify_slack(
        header_format=header_format,
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


@receiver(workflow_cancelled)
def notify_cancelled(sender, instance, user, **kwargs):
    message_format = ':heavy_multiplication_x: *{page_title}* ({page_type}) cancelled by {user_name}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


@receiver(workflow_approved)
def notify_approved(sender, instance, user, **kwargs):
    message_format = ':white_check_mark: *<{page_url}|{page_title}>* ({page_type}) approved by {user_name}{comment}'

    workflow_notify_slack(
        message_format=message_format,
        workflow_state=instance,
        user=user,
    )


@receiver(workflow_rejected)
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
    preview_url = settings.BASE_URL + reverse('wagtailadmin_pages:workflow_preview', args=(page.pk, workflow_state.current_task_state.task.pk))
    edit_url = settings.BASE_URL + reverse('wagtailadmin_pages:edit', args=(page.pk, ))
    workflow_history_url = settings.BASE_URL + reverse('wagtailadmin_pages:workflow_history_detail', args=(page.pk, workflow_state.pk))
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


@receiver(page_published)
def publication_notify_slack(sender, instance, revision, **kwargs):
    environment = get_environment_prefix()
    page = instance
    page_text = get_page_text(page)
    user_name = f'{revision.user.first_name} {revision.user.last_name}'
    restrictions_text = get_restrictions_text(page)

    latest_log_entry = PageLogEntry.objects.filter(page=page).order_by('-timestamp').first()

    # If this was not published via workflow approval (so that we don't send a duplicate notification)
    if latest_log_entry and latest_log_entry.action != 'wagtail.workflow.approve':
        # If this is the first time the page is being published
        if page.first_published_at == page.last_published_at:
            message = f'{environment}*<{page_text} published for the first time by {user_name}{restrictions_text}'
        else:
            message = f'{environment}*<{page_text} published by {user_name}{restrictions_text}'
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

# Could use PageViewRestriction as the sender, but:
# TODO: Make publication notification a part of this
# TODO: Add unpublish notification
@receiver(post_save, sender=PageLogEntry)
def log_entry_notify_slack(sender, instance, **kwargs):
    # TODO: Don't fetch this information if we're not going to send any messages
    environment = get_environment_prefix()
    page = instance.page
    page_text = get_page_text(page)
    user_name = f'{instance.user.first_name} {instance.user.last_name}'

    # TODO: Check whether the page is published. No need to notify about changing retrictions for draft pages.
    if instance.action == 'wagtail.view_restriction.edit':
        restrictions_text = get_restrictions_text(page)
        message = f'{environment}*<{page_text} made private by {user_name}{restrictions_text}'
    elif instance.action == 'wagtail.view_restriction.delete':
        message = f'{environment}*<{page_text} made public by {user_name}'
    else:
        message = ''

    if message:
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