from wagtail.core.models import Page
from django.db import models

class SubscribePage(Page):
    """
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = ['SubscriptionSegment',]

    class Meta:
        verbose_name = "New America Mailing List"

class SubscriptionSegment(Page):
    '''
        Subscription Segments imported from Campaign Monitor
    '''
    parent_page_types = ['SubscribePage',]
    SegmentID = models.TextField()
    ListID = models.TextField()
    is_creatable=False

    #alternative_title = models.TextField()

    class Meta:
        verbose_name = "Mailing List Segment"
