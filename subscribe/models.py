from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel


@register_snippet
class MailingListSegment(models.Model):
    title = models.TextField()

    class Meta:
        permissions = [
            ("can_sync_from_mailchimp", "Can sync from Mailchimp"),
        ]

    def __str__(self):
        return self.title


class SubscribePageSegmentPlacementQuerySet(models.QuerySet):
    def children_of(self, page_instance):
        from home.models import SubscribePage

        subscribe_page_ids = (
            page_instance.get_children()
            .type(SubscribePage)
            .live()
            .values_list("pk", flat=True)
        )
        return self.filter(page__pk__in=subscribe_page_ids)


class SubscribePageSegmentPlacement(Orderable, models.Model):
    page = ParentalKey(
        "home.SubscribePage",
        on_delete=models.CASCADE,
        related_name="segment_placements",
    )
    mailing_list_segment = models.ForeignKey(
        MailingListSegment, on_delete=models.CASCADE, related_name="+"
    )
    checked_by_default = models.BooleanField(
        default=True,
        help_text=(
            "If selected, this list will be checked when the subscribe page"
            " loads."
        ),
    )
    display_name = models.TextField(
        blank=True,
        default="",
        help_text=(
            "The name here will be used instead of the default name for this"
            " list."
        ),
    )

    @property
    def title(self):
        if self.display_name:
            return self.display_name
        return self.mailing_list_segment.title

    class Meta(Orderable.Meta):
        verbose_name = "mailing list segment placement"
        verbose_name_plural = "mailing list segment placements"
        constraints = [
            models.UniqueConstraint(
                fields=["page", "mailing_list_segment"],
                name="unique_list_page",
            )
        ]

    objects = SubscribePageSegmentPlacementQuerySet.as_manager()

    panels = [
        AutocompletePanel("mailing_list_segment"),
        FieldPanel("checked_by_default"),
        FieldPanel("display_name"),
    ]
