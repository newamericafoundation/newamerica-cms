import itertools

from django.core.management.base import BaseCommand

from home.models import SubscribePage, SubscriptionHomePageRelationship
from programs.models import (
    SubscriptionProgramRelationship,
    SubscriptionSubprogramRelationship,
)
from subscribe.models import MailingListSegment, SubscribePageSegmentPlacement


class Command(BaseCommand):
    help = "Convert SubscriptionSegments to MailingListSegment with a corresponding SubscribePage within its original Program, SubProgram, or HomePage."

    def handle(self, *args, **options):
        all_relationships = itertools.chain(
            SubscriptionHomePageRelationship.objects.all(),
            SubscriptionProgramRelationship.objects.all(),
            SubscriptionSubprogramRelationship.objects.all(),
        )

        for rel in all_relationships:
            parent_page = getattr(
                rel,
                "program",
                getattr(rel, "subprogram", None),
            )
            if not parent_page:
                self.stdout.write(f"Could not find parent page for {rel}")
                continue
            subscribe_page = SubscribePage.objects.child_of(parent_page).first()

            if not subscribe_page:
                subscribe_page = SubscribePage(
                    title="Subscribe",
                )
                parent_page.add_child(instance=subscribe_page)
            segment = rel.subscription_segment
            mailing_list_segment, _ = MailingListSegment.objects.get_or_create(
                title=segment.title,
            )
            display_name = getattr(
                rel,
                "alternate_name",
                getattr(
                    rel,
                    "alternate_title",
                    "",
                ),
            )
            SubscribePageSegmentPlacement.objects.get_or_create(
                page=subscribe_page,
                mailing_list_segment=mailing_list_segment,
                defaults={"display_name": display_name},
            )
