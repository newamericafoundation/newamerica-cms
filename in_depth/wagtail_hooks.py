from wagtail.core import hooks

from home.models import PublicationPermissions

from .models import InDepthProject, AllInDepthHomePage, InDepthProfile, InDepthSection


@hooks.register('construct_page_action_menu')
def remove_publish_in_depth_if_no_permission(menu_items, request, context):
    """Remove the 'Publish' action from all in depth projects unless the
    user is a superuser or in one of the auth groups specifically
    chosen for this permission.

    """
    page = context.get('page')
    parent_page = context.get('parent_page')

    editing_in_depth_page = (
        isinstance(page, InDepthProject)
        or isinstance(page, InDepthSection)
        or isinstance(page, InDepthProfile)
    )
    creating_in_depth_page = context.get('view') == 'create' and (
        isinstance(parent_page, AllInDepthHomePage)
        or isinstance(parent_page, InDepthProject)
    )
    if editing_in_depth_page or creating_in_depth_page:
        settings = PublicationPermissions.for_request(request)
        if request.user.is_superuser:
            # superusers can always publish
            return

        if not request.user.groups.all() & settings.groups_with_report_permission.all():
            menu_items[:] = [
                item for item in menu_items if item.name != 'action-publish'
            ]
