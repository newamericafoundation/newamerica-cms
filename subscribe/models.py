from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class SubscribePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['SubscriptionSegment']

    class Meta:
        verbose_name = "New America Mailing List"


class SubscriptionSegment(Page):
    '''
    Subscription Segments imported from Campaign Monitor
    '''

    parent_page_types = ['SubscribePage']
    SegmentID = models.TextField()
    ListID = models.TextField()
    is_creatable = False

    # alternative_title = models.TextField()

    class Meta:
        verbose_name = "Mailing List Segment"


@register_snippet
class MailingListSegment(models.Model):
    title = models.TextField()
    segment_id = models.TextField()
    list_id = models.TextField()
