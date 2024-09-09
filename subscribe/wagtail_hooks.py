from django.urls import include, path
from wagtail import hooks

from .views import mailchimp_sync_view


@hooks.register("register_admin_urls")
def register_commands_urls():
    return [
        path(
            "mailchimp/",
            include(
                (
                    [
                        path(
                            "",
                            mailchimp_sync_view,
                            name="sync",
                        )
                    ],
                    "mailchimp",
                ),
                namespace="mailchimp",
            ),
        )
    ]
