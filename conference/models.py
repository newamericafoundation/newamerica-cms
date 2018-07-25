from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from modelcluster.fields import ParentalKey

from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.embeds.blocks import EmbedBlock

from .blocks import VenueBlock, DirectionsBlock, PartnersBlock
from newamericadotorg.blocks import IntegerBlock, PeopleBlock, SessionsBlock

class AllConferencesHomePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['Conference']

    class Meta:
        verbose_name = "Conferences Homepage"

class Conference(Page):
    """
    """
    parent_page_types = ['AllConferencesHomePage']
    subpage_types = []

    description = RichTextField(help_text="This will be the ABOUT text")
    subheading = models.TextField(blank=True, null=True)
    story_excerpt = models.CharField("excerpt", blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Cover Image"
    )

    about_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="About Image"
    )

    alternate_logo = models.ForeignKey(
        'home.CustomImage',
        help_text="This will replace the New America logo at the top of the introduction / cover image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Alternate Logo"
    )

    host_organization = models.TextField(
        default='New America',
        blank=True,
        null=True
    )

    live_stream = models.URLField(blank=True, null=True)
    rsvp_link = models.URLField(blank=True, null=True)
    invitation_only = models.BooleanField(default=False, help_text="This will override the RSVP link and replace it with an request for invitation")
    publish_speakers = models.BooleanField(default=False, help_text="Speakers list will not show up until this is checked.")
    publish_sessions = models.BooleanField(default=False, help_text="Sessions list will not show up until this is checked.")

    date = models.DateField("Start Date", default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    location_name = models.TextField(help_text='Name of building (e.g. the Kennedy Center)', blank=True, null=True)
    street = models.TextField(default='740 15th St NW #900', blank=True, null=True)
    city = models.TextField(default='Washington', blank=True, null=True)
    state = models.TextField(default='D.C.', blank=True, null=True)
    zipcode = models.TextField(default='20005', blank=True, null=True)
    venue_details = RichTextField(null=True, blank=True)

    partner_heading = models.TextField(default='Sponsors & Partners')

    about = MultiFieldPanel(
        [
            FieldPanel('title'),
            FieldPanel('subheading'),
            FieldPanel('host_organization'),
            ImageChooserPanel('alternate_logo'),
            FieldRowPanel([
                FieldPanel('date', classname="col6"),
                FieldPanel('end_date', classname="col6")
            ]),
            ImageChooserPanel('story_image'),
            ImageChooserPanel('about_image'),
            FieldPanel('live_stream'),
            FieldPanel('description')
        ],
        heading="About"
    )

    setup = MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('rsvp_link', classname="col6"),
            FieldPanel('invitation_only', classname="col6"),
        ]),
        FieldRowPanel([
            FieldPanel('publish_speakers', classname="col6"),
            FieldPanel('publish_sessions', classname="col6")
        ])
    ], heading="Setup")

    address = MultiFieldPanel(
        [
            FieldPanel('location_name'),
            FieldPanel('street'),
            FieldPanel('city'),
            FieldRowPanel([
                FieldPanel('state', classname="col6"),
                FieldPanel('zipcode', classname="col6")
            ]),
            FieldPanel('venue_details'),
        ],
        heading="Conference Location"
    )

    hotel_location_name = models.TextField(help_text='Name of building (e.g. the Kennedy Center)', blank=True, null=True)
    hotel_street = models.TextField(default='740 15th St NW #900', blank=True, null=True)
    hotel_city = models.TextField(default='Washington', blank=True, null=True)
    hotel_state = models.TextField(default='D.C.', blank=True, null=True)
    hotel_zipcode = models.TextField(default='20005', blank=True, null=True)
    hotel_details = RichTextField(null=True, blank=True, help_text='must be filled for header and section to appear')

    hotel_address = MultiFieldPanel(
        [
            FieldPanel('hotel_location_name'),
            FieldPanel('hotel_street'),
            FieldPanel('hotel_city'),
            FieldRowPanel([
                FieldPanel('hotel_state', classname="col6"),
                FieldPanel('hotel_zipcode', classname="col6")
            ]),
            FieldPanel('hotel_details')
        ],
        heading="Hotel Location"
    )

    # to be deleted after transfer
    venue = StreamField(VenueBlock(), null=True, blank=True)
    directions = StreamField(DirectionsBlock(), null=True, blank=True)
    speakers = StreamField(PeopleBlock(), null=True, blank=True)
    partners = StreamField(PartnersBlock(), null=True, blank=True)
    sessions = StreamField(SessionsBlock(), null=True, blank=True)

    partners_and_sponsors = MultiFieldPanel([
        FieldPanel('partner_heading'),
        StreamFieldPanel('partners')
    ]);

    content_panels = [
        about,
        setup,
        address,
        hotel_address,
        StreamFieldPanel('directions'),
        StreamFieldPanel('speakers'),
        StreamFieldPanel('sessions'),
        partners_and_sponsors
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = 'Conference'
