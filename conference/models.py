import json

from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.wagtailcore.models import Page, Orderable

from home.models import Post
from blocks import PeopleBlock, SessionsBlock, VenueBlock, DirectionsBlock, PartnersBlock
from home.blocks import IntegerBlock

class AllConferencesHomePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['Conference']

    class Meta:
        verbose_name = "Homepage for all Conferences"

class Conference(Post):
    """
    """
    parent_page_types = ['AllConferencesHomePage']
    subpage_types = []

    description = RichTextField(help_text="This will be the ABOUT text", blank=True, null=True)
    host_organization = models.TextField(
        default='New America',
        blank=True,
        null=True
    )
    rsvp_link = models.URLField(blank=True, null=True)

    # date = models.DateField("Start Date")
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now, blank=True, null=True)

    street = models.TextField(default='740 15th St NW #900', blank=True, null=True)
    city = models.TextField(default='Washington', blank=True, null=True)
    state = models.TextField(default='D.C.', blank=True, null=True)
    zipcode = models.TextField(default='20005', blank=True, null=True)

    about = MultiFieldPanel(
        [
            FieldPanel('title'),
            FieldPanel('subheading'),
            FieldPanel('host_organization'),
            FieldPanel('description'),
            FieldPanel('rsvp_link')
        ],
        heading="About"
    )

    time = MultiFieldPanel(
        [
            FieldRowPanel([
                FieldPanel('date', classname="col6"),
                FieldPanel('end_date', classname="col6")
            ]),
            FieldRowPanel([
                FieldPanel('start_time', classname="col6"),
                FieldPanel('end_time', classname="col6")
            ])
        ],
        heading="Conference Days and Time"
    )

    address = MultiFieldPanel(
        [
            FieldPanel('street'),
            FieldPanel('city'),
            FieldRowPanel([
                FieldPanel('state', classname="col6"),
                FieldPanel('zipcode', classname="col6")
            ])
        ],
        heading="Conference Location"
    )

    venue = StreamField(VenueBlock(), null=True, blank=True)
    directions = StreamField(DirectionsBlock(), null=True, blank=True)
    speakers = StreamField(PeopleBlock(), null=True, blank=True)
    partners = StreamField(PartnersBlock(), null=True, blank=True)
    sessions = StreamField(SessionsBlock(), null=True, blank=True)

    content_panels = [
        about,
        time,
        address,
        StreamFieldPanel('venue'),
        StreamFieldPanel('directions'),
        StreamFieldPanel('speakers'),
        StreamFieldPanel('partners'),
        StreamFieldPanel('sessions')
        #InlinePanel('conference_sessions', label='Sessions'),
    ]

    promote_panels = Page.promote_panels


# # Sessions are a separate model
# # to allow fo querying and adding content to sessions separately
# # e.g adding video or audio links.
# class Session(models.Model):
#     name = models.TextField()
#     session_type = StreamField(SessionTypesBlock())
#     day = StreamField(IntegerChoiceBlock(help_text="What day of the conference is this session on?"))
#     description = RichTextField(blank=True,null=True)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     speakers = StreamField([
#         ('speaker', SessionSpeakerBlock())
#     ])
#
#     panels = [
#         FieldRowPanel([
#             FieldPanel('day', classname="col6"),
#         ]),
#         FieldPanel('name'),
#         FieldPanel('session_type'),
#         FieldPanel('description'),
#         FieldRowPanel([
#             FieldPanel('start_time', classname="col6"),
#             FieldPanel('end_time', classname="col6")
#         ])
#         #StreamFieldPanel('speakers')
#     ]
#
#     class Meta:
#         abstract = True
#
# # Makes session model available in editor
# # before new Conference is saved
# class ConferenceSession(Orderable,Session):
#     conference = ParentalKey('Conference', related_name='conference_sessions')
