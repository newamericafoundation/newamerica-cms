from wagtail.core import hooks

from home.models import PublicationPermissions

from .models import Report, ReportsHomepage


@hooks.register('construct_page_action_menu')
def remove_publish_report_if_no_permission(menu_items, request, context):
    """Remove the 'Publish' action from all reports unless the user is a
    superuser or in one of the auth groups specifically chosen for
    this permission.

    """
    editing_report_page = isinstance(context.get('page'), Report)
    creating_report_page = context.get('view') == 'create' and isinstance(
        context.get('parent_page'), ReportsHomepage
    )
    if editing_report_page or creating_report_page:
        settings = PublicationPermissions.for_request(request)
        if request.user.is_superuser:
            # superusers can always publish
            return

        if not request.user.groups.all() & settings.groups_with_report_permission.all():
            menu_items[:] = [
                item for item in menu_items if item.name != 'action-publish'
            ]
