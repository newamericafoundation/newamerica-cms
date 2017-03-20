from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailembeds.blocks import EmbedBlock

from blocks import VenueBlock, DirectionsBlock, PartnersBlock
from mysite.blocks import IntegerBlock, PeopleBlock, SessionsBlock

class AllConferencesHomePage(Page):
    parent_page_types = ['home.HomePage']
    subpage_types = ['Conference']

    class Meta:
        verbose_name = "Homepage for all Conferences"

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
        setup,
        address,
        StreamFieldPanel('venue'),
        StreamFieldPanel('directions'),
        StreamFieldPanel('speakers'),
        StreamFieldPanel('sessions'),
        StreamFieldPanel('partners')
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = 'Conference'
