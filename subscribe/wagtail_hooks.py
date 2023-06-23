from django.urls import include, path, reverse
from wagtail import hooks
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

from .views import campaign_monitor_sync_view


@hooks.register("register_admin_urls")
def register_commands_urls():
    return [
        path(
            "campaign_monitor/",
            include(
                (
                    [
                        path(
                            "",
                            campaign_monitor_sync_view,
                            name="sync",
                        )
                    ],
                    "campaign_monitor",
                ),
                namespace="campaign_monitor",
            ),
        )
    ]


@hooks.register("register_admin_menu_item")
def register_commands_menu_item():
    sync_menu_item = MenuItem(
        "Sync Campaign Monitor",
        reverse("campaign_monitor:sync"),
        classnames="icon icon-mail",
        order=10,
    )
    submenu = Menu(
        items=[
            sync_menu_item,
        ],
    )
    return SubmenuMenuItem("Commands", submenu, icon_name="code", order=10000)
