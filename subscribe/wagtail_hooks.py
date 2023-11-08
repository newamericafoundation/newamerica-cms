from django.urls import include, path
from wagtail import hooks

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
