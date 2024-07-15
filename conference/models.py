from django.db import models
from django.utils import timezone
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    TitleFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from newamericadotorg.blocks import PeopleBlock, SessionsBlock

from .blocks import DirectionsBlock, PartnersBlock, VenueBlock


class AllConferencesHomePage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["Conference"]

    class Meta:
        verbose_name = "Conferences Homepage"


class Conference(Page):
    """ """

    parent_page_types = ["AllConferencesHomePage"]
    subpage_types = []

    description = RichTextField(help_text="This will be the ABOUT text")
    subheading = models.TextField(blank=True, null=True)
    story_excerpt = models.CharField("excerpt", blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Cover Image",
    )
    story_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Cover image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    about_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="About Image",
    )
    about_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="About image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    alternate_logo = models.ForeignKey(
        "home.CustomImage",
        help_text="This will replace the New America logo at the top of the introduction / cover image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Alternate Logo",
    )
    alternate_logo_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Alternate logo alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )
    alternate_title_image = models.ForeignKey(
        "home.CustomImage",
        help_text="This will replace the title in the introduction / cover image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    alternate_title_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Alternate title image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    host_organization = models.TextField(default="New America", blank=True, null=True)

    live_stream = models.URLField(blank=True, null=True)
    rsvp_link = models.URLField(blank=True, null=True)
    invitation_only = models.BooleanField(
        default=False,
        help_text="This will override the RSVP link and replace it with an request for invitation",
    )
    publish_speakers = models.BooleanField(
        default=False, help_text="Speakers list will not show up until this is checked."
    )
    publish_sessions = models.BooleanField(
        default=False, help_text="Sessions list will not show up until this is checked."
    )

    date = models.DateField("Start Date", default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    location_name = models.TextField(
        help_text="Name of building (e.g. the Kennedy Center)", blank=True, null=True
    )
    street = models.TextField(default="740 15th St NW #900", blank=True, null=True)
    city = models.TextField(default="Washington", blank=True, null=True)
    state = models.TextField(default="D.C.", blank=True, null=True)
    zipcode = models.TextField(default="20005", blank=True, null=True)
    venue_details = RichTextField(null=True, blank=True)

    partner_heading = models.TextField(default="Sponsors & Partners")

    search_fields = Page.search_fields + [
        index.FilterField("date"),
    ]

    about = MultiFieldPanel(
        [
            TitleFieldPanel("title"),
            FieldPanel("subheading"),
            FieldPanel("host_organization"),
            FieldPanel("alternate_title_image"),
            FieldPanel("alternate_title_image_alt"),
            FieldPanel("alternate_logo"),
            FieldPanel("alternate_logo_alt"),
            FieldRowPanel(
                [
                    FieldPanel("date", classname="col6"),
                    FieldPanel("end_date", classname="col6"),
                ]
            ),
            FieldPanel("story_image"),
            FieldPanel("story_image_alt"),
            FieldPanel("about_image"),
            FieldPanel("about_image_alt"),
            FieldPanel("live_stream"),
            FieldPanel("description"),
        ],
        heading="About",
    )

    setup = MultiFieldPanel(
        [
            FieldRowPanel(
                [
                    FieldPanel("rsvp_link", classname="col6"),
                    FieldPanel("invitation_only", classname="col6"),
                ]
            ),
            FieldRowPanel(
                [
                    FieldPanel("publish_speakers", classname="col6"),
                    FieldPanel("publish_sessions", classname="col6"),
                ]
            ),
        ],
        heading="Setup",
    )

    address = MultiFieldPanel(
        [
            FieldPanel("location_name"),
            FieldPanel("street"),
            FieldPanel("city"),
            FieldRowPanel(
                [
                    FieldPanel("state", classname="col6"),
                    FieldPanel("zipcode", classname="col6"),
                ]
            ),
            FieldPanel("venue_details"),
        ],
        heading="Conference Location",
    )

    hotel_location_name = models.TextField(
        help_text="Name of building (e.g. the Kennedy Center)", blank=True, null=True
    )
    hotel_street = models.TextField(
        default="740 15th St NW #900", blank=True, null=True
    )
    hotel_city = models.TextField(default="Washington", blank=True, null=True)
    hotel_state = models.TextField(default="D.C.", blank=True, null=True)
    hotel_zipcode = models.TextField(default="20005", blank=True, null=True)
    hotel_details = RichTextField(
        null=True,
        blank=True,
        help_text="must be filled for header and section to appear",
    )

    hotel_address = MultiFieldPanel(
        [
            FieldPanel("hotel_location_name"),
            FieldPanel("hotel_street"),
            FieldPanel("hotel_city"),
            FieldRowPanel(
                [
                    FieldPanel("hotel_state", classname="col6"),
                    FieldPanel("hotel_zipcode", classname="col6"),
                ]
            ),
            FieldPanel("hotel_details"),
        ],
        heading="Hotel Location",
    )

    # to be deleted after transfer
    venue = StreamField(VenueBlock(), null=True, blank=True, use_json_field=True)
    directions = StreamField(
        DirectionsBlock(), null=True, blank=True, use_json_field=True
    )
    speakers = StreamField(PeopleBlock(), null=True, blank=True, use_json_field=True)
    partners = StreamField(PartnersBlock(), null=True, blank=True, use_json_field=True)
    sessions = StreamField(SessionsBlock(), null=True, blank=True, use_json_field=True)

    partners_and_sponsors = MultiFieldPanel(
        [FieldPanel("partner_heading"), FieldPanel("partners")]
    )

    content_panels = [
        about,
        setup,
        address,
        hotel_address,
        FieldPanel("directions"),
        FieldPanel("speakers"),
        FieldPanel("sessions"),
        partners_and_sponsors,
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = "Conference"
