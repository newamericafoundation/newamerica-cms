import json

from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from home.models import Post
from programs.models import Program, Subprogram
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.models import Page, Orderable
from modelcluster.fields import ParentalKey

from blocks import SessionSpeakerBlock
from home.blocks import IntegerBlock

class AllConferencesHomePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['Post']

    class Meta:
        verbose_name = "Homepage for all Conferences"

class Conference(Post):
    """
    """
    parent_page_types = ['AllConferencesHomePage']
    subpage_types = []

    host_organization = models.TextField(
        default='New America',
        blank=True,
        null=True
    )

    rsvp_link = models.URLField(blank=True)

    date = models.DateField("Start Date",required=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now, blank=True, null=True)

    street = models.TextField(default='740 15th St NW #900')
    city = models.TextField(default='Washington')
    state = models.TextField(default='D.C.')
    zipcode = models.TextField(default='20005')

    time = MultiFieldPanel(
        [
            FieldRowPanel(['date','end_date']),
            FieldRowPanel(['start_time','end_time'])
        ]
        heading="Conference Days and Time"
    )
    address = MultiFieldPanel(
        [
            FieldPanel('street'),
            FieldRowPanel(['city','state','zipcode'])
        ],
        heading="Conference Location"
    )

    content_panels = Post.content_panels + [
        time,
        address,
        InlinePanel('session', label="Sessions"),
        FieldPanel('rsvp_link'),
        FieldPanel('host_organization')
    ]


SESSION_TYPES = (
    ('panel', 'Panel'),
    ('speaker', 'Speaker'),
    ('break', 'Break'),
    ('meal', 'Meal'),
    ('reception','Reception'),
    ('registration', 'Registration'),
)

# Sessions are a separate model
# to allow fo querying and adding content to sessions separately
# e.g adding video or audio links.
class Session(model.Models):
    name = models.TextField(required=True)
    session_type = models.TextField(required=True,choices=SESSION_TYPES)
    day = IntegerBlock(help_text="What day of the conference is this on?")
    description = models.RichTextField()
    start_time = models.TimeField(required=True)
    end_time = models.TimeField(required=True)
    speakers = StreamField([
        ('speaker', SessionSpeakerBlock())
    ])

    panels = [
        FieldPanel('name'),
        FieldPanel('session_type'),
        FieldPanel('day'),
        FieldPanel('description'),
        FieldRowPanel(['start_time','end_time']),
        StreamFieldPanel('speakers')
    ]

    class Meta:
        abstract = True

# Makes session model available in editor
# before new Conference is saved
class ConferenceSessions(Orderable,Session):
    conference = ParentalKey(Conference, related_name='session')
