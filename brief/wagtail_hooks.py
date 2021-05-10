from wagtail.core import hooks

from home.models import PublicationPermissions

from .models import Brief, ProgramBriefsPage


@hooks.register('construct_page_action_menu')
def remove_publish_brief_if_no_permission(menu_items, request, context):
    """Remove the 'Publish' action from all briefs unless the user is a
    superuser or in one of the auth groups specifically chosen for
    this permission.

    """
    editing_brief_page = isinstance(context.get('page'), Brief)
    creating_brief_page = context.get('view') == 'create' and isinstance(
        context.get('parent_page'), ProgramBriefsPage
    )
    if editing_brief_page or creating_brief_page:
        settings = PublicationPermissions.for_request(request)
        if request.user.is_superuser:
            # superusers can always publish
            return

        if not request.user.groups.all() & settings.groups_with_brief_permission.all():
            menu_items[:] = [
                item for item in menu_items if item.name != 'action-publish'
            ]
