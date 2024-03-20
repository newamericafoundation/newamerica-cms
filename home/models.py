import json
from datetime import datetime

import django.db.models.options as options
from django.apps import apps
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from pytz import timezone
from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    TitleFieldPanel,
)
from wagtail.blocks import PageChooserBlock
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import Page
from wagtail.search import index
from wagtail_headless_preview.models import HeadlessPreviewMixin, PagePreview

from newamericadotorg.blocks import BodyBlock
from newamericadotorg.wagtailadmin.widgets import LocationWidget
from person.models import Person
from programs.models import AbstractProgram, Program, Subprogram
from subscribe.models import SubscribePageSegmentPlacement

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("description",)


class RedirectHeadlessPreviewMixin(HeadlessPreviewMixin):
    def serve_preview(self, request, mode_name):
        use_live_preview = request.GET.get("live_preview")
        token = request.COOKIES.get("used-token")

        if use_live_preview and token:
            page_preview, existed = self.update_page_preview(token)
            PagePreview.garbage_collect()

            # Imported locally as live preview is optional
            from wagtail_headless_preview.signals import (
                preview_update,
            )

            preview_update.send(sender=HeadlessPreviewMixin, token=token)
        else:
            PagePreview.garbage_collect()
            page_preview = self.create_page_preview()
            page_preview.save()

        response_token = token or page_preview.token

        response = redirect(self.get_preview_url(response_token))

        return response


class CustomImage(AbstractImage):
    # Add any extra fields to image here

    source = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        "source",
        "caption",
    )

    def get_url(self):
        try:
            return self.url
        except Exception:
            return None


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


## unnecessary with wagtail 1.10
# # Delete the source image file when an image is deleted
# @receiver(pre_delete, sender=CustomImage)
# def image_delete(sender, instance, **kwargs):
#     instance.file.delete(False)
#
#
# # Delete the rendition image file when a rendition is deleted
# @receiver(pre_delete, sender=CustomRendition)
# def rendition_delete(sender, instance, **kwargs):
#     instance.file.delete(False)


class HomePage(Page):
    """
    Model for the homepage for the website. In Wagtail's parent
    child structure, this is the most parent page.
    """

    subpage_types = [
        "OrgSimplePage",
        "programs.Program",
        "article.AllArticlesHomePage",
        "weekly.Weekly",
        "weekly.AllWeeklyArticlesHomePage",
        "the_thread.Thread",
        "the_thread.AllThreadArticlesHomePage",
        "event.AllEventsHomePage",
        "conference.AllConferencesHomePage",
        "blog.AllBlogPostsHomePage",
        "book.AllBooksHomePage",
        "person.OurPeoplePage",
        "person.BoardAndLeadershipPeoplePage",
        "podcast.AllPodcastsHomePage",
        "policy_paper.AllPolicyPapersHomePage",
        "brief.AllBriefsHomePage",
        "press_release.AllPressReleasesHomePage",
        "quoted.AllQuotedHomePage",
        "in_depth.AllInDepthHomePage",
        "JobsPage",
        "RedirectPage",
        "home.SubscribePage",
        "programs.PublicationsPage",
        "report.AllReportsHomePage",
        "other_content.AllOtherPostsHomePage",
        "collection.Collection",
        "collection.CollectionsHomePage",
    ]

    down_for_maintenance = models.BooleanField(default=False)

    # Up to four lead stories can be featured on the homepage.
    # Lead_1 will be featured most prominently.
    lead_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    lead_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    lead_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    lead_4 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Up to three featured stories to appear underneath
    # the lead stories. All of the same size and formatting.
    feature_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    feature_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    feature_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    featured_stories = [feature_1, feature_2, feature_3]

    about_pages = StreamField(
        [
            ("page", PageChooserBlock()),
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("about_pages")]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("lead_1"),
                FieldPanel("lead_2"),
                FieldPanel("lead_3"),
                FieldPanel("lead_4"),
            ],
            heading="Lead Stories",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("feature_1"),
                FieldPanel("feature_2"),
                FieldPanel("feature_3"),
            ],
            heading="Featured Stories",
            classname="collapsible",
        ),
    ]

    settings_panels = Page.settings_panels + [FieldPanel("down_for_maintenance")]

    def get_subscription_segments(self):
        return SubscribePageSegmentPlacement.objects.children_of(self)

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # In order to apply different styling to main lead story
        # versus the other lead stories, we needed to separate them out
        context["other_lead_stories"] = []

        # Solution to account for null values for the stories
        # so that the div in the template wouldn't attempt to add styling to nothing
        if self.lead_2:
            context["other_lead_stories"].append(self.lead_2)
        if self.lead_3:
            context["other_lead_stories"].append(self.lead_3)
        if self.lead_4:
            context["other_lead_stories"].append(self.lead_4)

        # In order to preserve style, minimum and maximum of feature stories is 3
        # If there are less than 3 feature stories - none show up even if they're added.
        if self.feature_1 and self.feature_2 and self.feature_3:
            context["featured_stories"] = [
                self.feature_1,
                self.feature_2,
                self.feature_3,
            ]
        else:
            context["featured_stories"] = []

        # uses get_model instead of traditional import to avoid circular import
        Event = apps.get_model("event", "Event")

        eastern = timezone("US/Eastern")
        curr_time = datetime.now(eastern).time()
        curr_date = datetime.now(eastern).date()
        date_filter = Q(date__gt=curr_date) | (
            Q(date=curr_date) & Q(start_time__gte=curr_time)
        )

        context["upcoming_events"] = (
            Event.objects.live()
            .public()
            .filter(date_filter)
            .order_by("date", "start_time")[:3]
        )
        context["recent_publications"] = (
            Post.objects.live()
            .public()
            .specific()
            .not_type(Event)
            .order_by("-date")[:4]
        )

        return context

    class Meta:
        verbose_name = "Homepage"


class AbstractSimplePage(Page):
    """
    Abstract Simple page class that inherits from the Page model and
    creates simple, generic pages.
    """

    body = StreamField(
        BodyBlock(required=False), blank=True, null=True, use_json_field=True
    )
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)
    custom_interface = models.BooleanField(default=False)
    story_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    story_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Story image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    data_project_external_script = models.CharField(
        blank=True,
        null=True,
        max_length=140,
        help_text="Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.",
    )

    content_panels = Page.content_panels + [FieldPanel("body")]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_excerpt"),
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("data_project_external_script"),
        FieldPanel("custom_interface"),
    ]

    class Meta:
        abstract = True


class RedirectPage(Page):
    """
    Redirect page class that inherits from the Page model and
    overrides the serve method to allow for redirects to pages
    external to the site.
    """

    preview_modes = []

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    story_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Story image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )
    redirect_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("redirect_url"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_excerpt"),
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]

    def serve(self, request):
        return redirect(self.redirect_url, permanent=True)

    class Meta:
        verbose_name = "External Website"


class OrgSimplePage(AbstractSimplePage):
    """
    Simple Page at the organization level
    """

    parent_page_types = ["home.HomePage", "OrgSimplePage", "JobsPage"]
    subpage_types = ["OrgSimplePage", "home.RedirectPage"]

    page_description = RichTextField(blank=True)

    content_panels = [
        MultiFieldPanel(
            [
                TitleFieldPanel("title"),
                FieldPanel("page_description"),
            ]
        ),
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super(OrgSimplePage, self).get_context(request)
        if self.custom_interface is True:
            context["template"] = "home/custom_simple_interface.html"
        else:
            context["template"] = "post_page.html"

        return context

    class Meta:
        verbose_name = "About Page"


class ProgramSimplePage(AbstractSimplePage):
    """
    Simple Page at the Program level
    """

    parent_page_types = ["programs.Program", "programs.Subprogram"]
    subpage_types = ["home.RedirectPage"]

    @cached_property
    def program(self):
        return self.get_parent().specific

    def get_context(self, request):
        context = super(ProgramSimplePage, self).get_context(request)
        context["program"] = self.program

        return context

    class Meta:
        verbose_name = "About Page"


class ProgramAboutHomePage(RedirectHeadlessPreviewMixin, ProgramSimplePage):
    parent_page_types = ["programs.Program", "programs.Subprogram", "programs.Project"]
    subpage_types = ["home.ProgramAboutPage"]

    class Meta:
        verbose_name = "About Homepage"

    def get_context(self, request):
        context = super().get_context(request)

        if getattr(request, "is_preview", False):
            program_context = context["program"].get_context(request)
            context["initial_state"] = program_context["initial_state"]
            context["initial_topics_state"] = program_context["initial_topics_state"]

        return context

    def clean_fields(self, *args, **kwargs):
        if self.slug != "about":
            self.slug = "about"
        super().clean_fields(*args, **kwargs)


class ProgramAboutPage(RedirectHeadlessPreviewMixin, ProgramSimplePage):
    parent_page_types = ["home.ProgramAboutHomePage"]
    subpage_types = ["home.ProgramSimplePage"]

    class Meta:
        verbose_name = "Program About Page"

    @cached_property
    def program(self):
        return (
            Page.objects.ancestor_of(self)
            .type(AbstractProgram)
            .order_by("-depth")
            .first()
            .specific
        )

    def get_context(self, request):
        context = super().get_context(request)
        context["program"] = self.program

        if getattr(request, "is_preview", False):
            program_context = context["program"].get_context(request)
            context["initial_state"] = program_context["initial_state"]
            context["initial_topics_state"] = program_context["initial_topics_state"]

        return context


class JobsPage(OrgSimplePage):
    """
    Jobs Page at the organization level
    """

    class Meta:
        verbose_name = "Jobs Page"


class SubscribePage(OrgSimplePage):
    """
    Subscribe Page at the organization level
    """

    parent_page_types = [
        "home.HomePage",
        "programs.Program",
        "programs.Subprogram",
        "the_thread.Thread",
    ]

    newsletter_subscriptions = StreamField(
        [
            (
                "subscription",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True)),
                        (
                            "description",
                            blocks.CharBlock(required=False, max_length=120),
                        ),
                        (
                            "id",
                            blocks.CharBlock(
                                required=True,
                                max_length=6,
                                help_text="Enter the unique campaign monitor ID",
                            ),
                        ),
                        # ('checked_by_default', blocks.BooleanBlock(default=False, required=False, help_text="Controls whether subscription is checked by default on the Subscribe Page"))
                    ],
                    icon="placeholder",
                ),
            )
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    event_subscriptions = StreamField(
        [
            (
                "subscription",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True)),
                        (
                            "description",
                            blocks.CharBlock(required=False, max_length=120),
                        ),
                        (
                            "id",
                            blocks.CharBlock(
                                required=True,
                                max_length=6,
                                help_text="Enter the unique campaign monitor ID",
                            ),
                        ),
                        # ('checked_by_default', blocks.BooleanBlock(default=False, required=False, help_text="Controls whether subscription is checked by default on the Subscribe Page"))
                    ],
                    icon="placeholder",
                ),
            )
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        InlinePanel("segment_placements", label="Mailing List Segments", min_num=1),
    ]

    class Meta:
        verbose_name = "Subscribe Page"

    def get_context(self, request):
        from newamericadotorg.api.program.serializers import (
            MailingListPlacementSerializer,
        )

        context = super().get_context(request)
        parent_class = self.get_parent().specific_class
        context["is_org_wide"] = parent_class == HomePage
        context["subscriptions"] = json.dumps(
            [
                MailingListPlacementSerializer(s).data for s in self.segment_placements.all()
            ]
        )
        return context


class PostAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Authors
    """

    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="+")
    post = ParentalKey("Post", related_name="authors")

    panels = [
        FieldPanel("author"),
    ]

    class Meta:
        ordering = ["pk"]


class PostProgramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Programs
    """

    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="+")
    post = ParentalKey("Post", related_name="programs")

    panels = [
        FieldPanel("program"),
    ]

    class meta:
        unique_together = (("program", "post"),)

    def __str__(self):
        return str(self.program) + "," + str(self.post)


class PostSubprogramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Subprograms
    """

    subprogram = models.ForeignKey(
        Subprogram, on_delete=models.CASCADE, related_name="+"
    )
    post = ParentalKey("Post", related_name="subprograms")

    panels = [
        FieldPanel("subprogram"),
    ]

    class meta:
        unique_together = (("subprogram", "post"),)


class PostTopicRelationship(models.Model):
    topic = models.ForeignKey(
        "issue.IssueOrTopic", on_delete=models.CASCADE, related_name="+"
    )
    post = ParentalKey("home.Post", related_name="topics")

    panels = [PageChooserPanel("topic", "issue.IssueOrTopic")]


class Location(models.Model):
    location = models.CharField(max_length=999)
    formatted_address = models.CharField(max_length=999, blank=True, null=True)
    street_number = models.CharField(max_length=999, blank=True, null=True)
    street = models.CharField(max_length=999, blank=True, null=True)
    city = models.CharField(max_length=999, blank=True, null=True)
    state_or_province = models.CharField(max_length=999, blank=True, null=True)
    zipcode = models.CharField(max_length=999, blank=True, null=True)
    county = models.CharField(max_length=999, blank=True, null=True)
    country = models.CharField(max_length=999, blank=True, null=True)
    latitude = models.CharField(max_length=999, blank=True, null=True)
    longitude = models.CharField(max_length=999, blank=True, null=True)

    post = ParentalKey("Post", related_name="location", blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("location", widget=LocationWidget),
                FieldPanel("formatted_address", classname="disabled-input"),
                FieldPanel(
                    "street_number",
                    classname="disabled-input field-col col6",
                ),
                FieldPanel("street", classname="disabled-input field-col col6"),
                FieldPanel("county", classname="disabled-input field-col col6"),
                FieldPanel("zipcode", classname="disabled-input field-col col6"),
                FieldPanel("city", classname="disabled-input field-col col12"),
                FieldPanel(
                    "state_or_province", classname="disabled-input field-col col12"
                ),
                FieldPanel("country", classname="disabled-input field-col col12"),
                FieldPanel("latitude", classname="disabled-input field-col col6"),
                FieldPanel("longitude", classname="disabled-input field-col col6"),
            ]
        )
    ]


class Post(Page):
    """
    Abstract Post class that inherits from Page
    and provides a model template for other content
    type models
    """

    subheading = models.TextField(blank=True, null=True)

    date = models.DateField("Post date")

    # A unique string based on the publish date and id, which is set during save
    # used to determine ordering for pagination in the "post" api
    ordered_date_string = models.CharField(blank=True, max_length=140)

    body = StreamField(
        BodyBlock(required=False), blank=True, null=True, use_json_field=True
    )

    parent_programs = models.ManyToManyField(
        Program, through=PostProgramRelationship, blank=True
    )

    post_subprogram = models.ManyToManyField(
        Subprogram, through=PostSubprogramRelationship, blank=True
    )

    post_author = models.ManyToManyField(
        Person, through=PostAuthorRelationship, blank=True
    )

    post_topic = models.ManyToManyField(
        "issue.IssueOrTopic", through=PostTopicRelationship, blank=True
    )

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    story_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Story image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    data_project_external_script = models.CharField(
        blank=True,
        null=True,
        max_length=140,
        help_text="Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subheading"),
        FieldPanel("date"),
        FieldPanel("body"),
        InlinePanel("programs", label=("Programs")),
        InlinePanel("subprograms", label=("Subprograms")),
        InlinePanel("authors", label=("Authors")),
        InlinePanel("topics", label=("Topics")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_excerpt"),
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
        InlinePanel(
            "location",
            label=("Locations"),
        ),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("data_project_external_script"),
    ]

    is_creatable = False

    search_fields = Page.search_fields + [
        index.SearchField("body", boost=0.5),
        index.AutocompleteField("body", boost=0.5),
        index.FilterField("date"),
        index.RelatedFields(
            "parent_programs",
            [
                index.SearchField("name"),
                index.AutocompleteField("name"),
            ],
        ),
        index.RelatedFields(
            "post_author",
            [
                index.SearchField("first_name"),
                index.AutocompleteField("first_name"),
                index.SearchField("last_name"),
                index.AutocompleteField("last_name"),
                index.SearchField("position_at_new_america"),
                index.AutocompleteField("position_at_new_america"),
            ],
        ),
    ]

    def get_context(self, request):
        context = super(Post, self).get_context(request)
        context["authors"] = self.authors.order_by("pk")

        return context

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program - post relationship is
        captured even if the user does not select it.
        """

        # This line fills the date ordering field with the publish date
        # plus the post id, to create a unique string by which to order posts
        self.ordered_date_string = f"{str(self.date)}-{self.id}"

        super(Post, self).save(*args, **kwargs)

        program = Program.objects.ancestor_of(self).first()
        if program:
            relationship, created = PostProgramRelationship.objects.get_or_create(
                program=program, post=self
            )
            if created:
                relationship.save()

            subprogram = Subprogram.objects.ancestor_of(self).first()
            if subprogram:
                (
                    relationship,
                    created,
                ) = PostSubprogramRelationship.objects.get_or_create(
                    subprogram=subprogram.specific, post=self
                )
                if created:
                    relationship.save()


class AbstractHomeContentPage(Page):
    """
    Convenience Class for querying all Content homepages
    """

    class Meta:
        abstract = True


@register_setting(icon="placeholder")
class PublicationPermissions(BaseSiteSetting, ClusterableModel):
    groups_with_report_permission = ParentalManyToManyField(
        Group,
        blank=True,
        related_name="+",
        help_text='Group that has permission to perform the "Publish" action on Report pages. Only superusers and users that are members of the group selected here may do so, otherwise reports must go through the applicable workflow.',
    )
    groups_with_brief_permission = ParentalManyToManyField(
        Group,
        blank=True,
        related_name="+",
        help_text='Group that has permission to perform the "Publish" action on Brief pages. Only superusers and users that are members of the group selected here may do so, otherwise reports must go through the applicable workflow.',
    )

    panels = [
        FieldPanel("groups_with_report_permission"),
        FieldPanel("groups_with_brief_permission"),
    ]
