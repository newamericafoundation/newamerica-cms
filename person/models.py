from django.db import models
from django import forms

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.blocks import URLBlock
from wagtail.fields import RichTextField
from wagtail.admin.panels import PageChooserPanel, MultiFieldPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey

from programs.models import Program, Subprogram, AbstractContentPage

from newamericadotorg.helpers import paginate_results

import datetime

ROLE_OPTIONS = (
    ("Board Chair", "Board Chair"),
    ("Board Member", "Board Member"),
    ("Fellow", "Fellow"),
    ("Central Staff", "Central Staff"),
    ("Program Staff", "Program Staff"),
    ("External Author/Former Staff", "External Author"),
)
GROUPING_OPTIONS = (
    ("Current Fellows", "Current Fellows"),
    ("Former Fellows", "Former Fellows"),
    ("Advisors", "Advisors"),
    ("Contributing Staff", "Contributing Staff"),
)
YEAR_CHOICES = [(r, r) for r in range(1999, datetime.date.today().year + 1)]
YEAR_CHOICES.reverse()


# Through relationship that connects the Person model
# to the Program model so that a Person may belong
# to more than one Program
class PersonProgramRelationship(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="+")
    person = ParentalKey("Person", related_name="programs")
    group = models.CharField(
        choices=GROUPING_OPTIONS,
        max_length=50,
        blank=True,
        null=True,
        help_text="Set grouping for program's our people page",
    )
    fellowship_position = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Set program-specific fellowship information",
    )
    fellowship_year = models.IntegerField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "Used for ordering this person on the Program page. "
            "People with a lower sort order will appear first."
        ),
    )
    panels = [
        FieldPanel("program"),
        FieldPanel("group"),
        FieldPanel("fellowship_position"),
        FieldPanel(
            "fellowship_year",
            widget=forms.Select(choices=YEAR_CHOICES),
            classname="typed_choice_field",
        ),
        FieldPanel("sort_order"),
    ]


# Through relationship that connects the Person model
# to the Subprogram model so that a Person may belong
# to more than one Subprogram
class PersonSubprogramRelationship(models.Model):
    subprogram = models.ForeignKey(
        Subprogram, on_delete=models.CASCADE, related_name="+"
    )
    person = ParentalKey("Person", related_name="subprograms")
    group = models.CharField(
        choices=GROUPING_OPTIONS,
        max_length=50,
        blank=True,
        null=True,
        help_text="Set grouping for subprogram's our people page",
    )
    fellowship_position = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Set subprogram-specific fellowhip information",
    )
    fellowship_year = models.IntegerField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "Used for ordering this person on the Program page. "
            "People with a lower sort order will appear first."
        ),
    )
    panels = [
        FieldPanel("subprogram"),
        FieldPanel("group"),
        FieldPanel("fellowship_position"),
        FieldPanel(
            "fellowship_year",
            widget=forms.Select(choices=YEAR_CHOICES),
            classname="typed_choice_field",
        ),
        FieldPanel("sort_order"),
    ]


class PersonTopicRelationship(models.Model):
    topic = models.ForeignKey(
        "issue.IssueOrTopic", on_delete=models.CASCADE, related_name="+"
    )
    person = ParentalKey("person.Person", related_name="topics")

    panels = [PageChooserPanel("topic", "issue.IssueOrTopic")]


class Person(Page):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    position_at_new_america = models.CharField(
        max_length=500,
        help_text="Position or Title at New America",
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=True, null=True)
    short_bio = RichTextField(blank=True, null=True)
    long_bio = RichTextField(blank=True, null=True)
    expert = models.BooleanField(default=False)
    leadership = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "Used for ordering this person on the Our People page. "
            "People with a lower sort order will appear first."
        ),
    )
    profile_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    profile_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Profile image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    belongs_to_these_programs = models.ManyToManyField(
        Program, through=PersonProgramRelationship, blank=True
    )

    belongs_to_these_subprograms = models.ManyToManyField(
        Subprogram,
        through=PersonSubprogramRelationship,
        blank=True,
    )

    expertise = models.ManyToManyField(
        "issue.IssueOrTopic",
        through=PersonTopicRelationship,
        blank=True,
    )

    social_media = StreamField(
        [
            (
                "twitter",
                URLBlock(required=False, help_text="Twitter Profile Link", icon="user"),
            ),
            (
                "facebook",
                URLBlock(required=False, help_text="Facebook Profile", icon="user"),
            ),
            (
                "youtube",
                URLBlock(required=False, help_text="YouTube Channel", icon="media"),
            ),
            (
                "google_plus",
                URLBlock(required=False, help_text="Google+ Profile", icon="user"),
            ),
            (
                "linkedin",
                URLBlock(required=False, help_text="LinkedIn Profile", icon="user"),
            ),
            ("tumblr", URLBlock(required=False, help_text="Tumblr", icon="user")),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    role = models.CharField(choices=ROLE_OPTIONS, max_length=50)
    former = models.BooleanField(
        default=False, help_text="Select if person no longer serves above role."
    )
    fellowship_year = models.IntegerField(blank=True, null=True)
    # Up to three featured work pages to appear on bio page
    feature_work_1 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    feature_work_2 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    feature_work_3 = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("first_name"),
                FieldPanel("last_name"),
                FieldPanel("profile_image"),
                FieldPanel("profile_image_alt"),
                FieldPanel("short_bio"),
                FieldPanel("long_bio", classname="full"),
            ],
            heading="About",
        ),
        MultiFieldPanel(
            [
                FieldPanel("position_at_new_america"),
                FieldPanel("role"),
                FieldPanel("former"),
                FieldPanel(
                    "fellowship_year",
                    widget=forms.Select(choices=YEAR_CHOICES),
                    classname="typed_choice_field",
                ),
                FieldPanel("expert"),
                FieldPanel("leadership"),
                FieldPanel("sort_order"),
            ],
            heading="Role",
        ),
        InlinePanel("programs", label=("Belongs to these Programs")),
        InlinePanel("subprograms", label=("Belongs to these Subprograms/Initiatives")),
        InlinePanel("topics", label="Expert in these topics"),
        MultiFieldPanel(
            [FieldPanel("email"), FieldPanel("social_media")], heading="Contact"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel(
                    "feature_work_1",
                    [
                        "article.Article",
                        "blog.BlogPost",
                        "book.Book",
                        "brief.Brief",
                        "event.Event",
                        "issue.IssueOrTopic",
                        "podcast.Podcast",
                        "policy_paper.PolicyPaper",
                        "press_release.PressRelease",
                        "quoted.Quoted",
                        "weekly.WeeklyArticle",
                        "the_thread.ThreadArticle",
                        "report.Report",
                        "in_depth.InDepthProject",
                        "other_content.OtherPost",
                    ],
                ),
                PageChooserPanel(
                    "feature_work_2",
                    [
                        "article.Article",
                        "blog.BlogPost",
                        "book.Book",
                        "brief.Brief",
                        "event.Event",
                        "issue.IssueOrTopic",
                        "podcast.Podcast",
                        "policy_paper.PolicyPaper",
                        "press_release.PressRelease",
                        "quoted.Quoted",
                        "weekly.WeeklyArticle",
                        "the_thread.ThreadArticle",
                        "report.Report",
                        "in_depth.InDepthProject",
                        "other_content.OtherPost",
                    ],
                ),
                PageChooserPanel(
                    "feature_work_3",
                    [
                        "article.Article",
                        "blog.BlogPost",
                        "book.Book",
                        "brief.Brief",
                        "event.Event",
                        "issue.IssueOrTopic",
                        "podcast.Podcast",
                        "policy_paper.PolicyPaper",
                        "press_release.PressRelease",
                        "quoted.Quoted",
                        "weekly.WeeklyArticle",
                        "the_thread.ThreadArticle",
                        "report.Report",
                        "in_depth.InDepthProject",
                        "other_content.OtherPost",
                    ],
                ),
            ],
            heading="Featured Work To Highlight on Bio Page",
            classname="collapsible",
        ),
    ]

    parent_page_types = ["OurPeoplePage"]
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField("position_at_new_america", boost=0.33),
        index.SearchField("long_bio", boost=0.01),
        index.SearchField("short_bio", boost=0.33),
        index.SearchField("role", boost=0.01),
        index.RelatedFields(
            "belongs_to_these_programs",
            [
                index.SearchField("name"),
            ],
        ),
        index.RelatedFields(
            "belongs_to_these_subprograms",
            [
                index.SearchField("name"),
            ],
        ),
        index.FilterField("former"),
    ]

    def get_context(self, request):
        context = super(Person, self).get_context(request)
        featured_work = [self.feature_work_1, self.feature_work_2, self.feature_work_3]

        context["featured_work"] = featured_work

        # Returns posts that the person has authored ordered by date
        context["posts"] = paginate_results(
            request, self.post_set.live().order_by("-date")
        )

        return context

    class Meta:
        ordering = ("last_name",)
        verbose_name = "Person"


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns everyone from the Person model
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = ["Person", "BoardAndLeadershipPeoplePage"]

    page_description = RichTextField(blank=True, null=True)

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

    content_panels = Page.content_panels + [
        FieldPanel("page_description"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]

    def get_context(self, request):
        context = super(OurPeoplePage, self).get_context(request)
        context["ourpeoplepage"] = OurPeoplePage.objects.filter(
            slug="our-people"
        ).first()

        return context

    class Meta:
        verbose_name = "Our People Page"


class ExpertPage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone who is marked as an expert from the Person model
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    page_description = RichTextField(blank=True, null=True)
    contact_information = RichTextField(blank=True, null=True)

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

    content_panels = Page.content_panels + [
        FieldPanel("page_description"),
        FieldPanel("contact_information"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]


class ProgramPeoplePage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """

    parent_page_types = ["programs.Program", "programs.Subprogram", "programs.Project"]
    subpage_types = []

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

    promote_panels = Page.promote_panels + [
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]

    class Meta:
        verbose_name = "Our People Page"


class BoardAndLeadershipPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """

    parent_page_types = ["home.HomePage", "OurPeoplePage"]
    subpage_types = []

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

    page_description = RichTextField(blank=True, null=True)

    QUERY_OPTIONS = (
        ("Board Member", "Board Members"),
        ("Leadership Team", "Leadership Team"),
        ("Central Staff", "Central Staff"),
    )
    role_query = models.CharField(
        choices=QUERY_OPTIONS, max_length=50, default="Board Members"
    )
    former_query = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel("page_description"),
        FieldPanel("role_query"),
        FieldPanel("former_query"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("story_image"),
        FieldPanel("story_image_alt"),
    ]

    def get_context(self, request):
        context = super(BoardAndLeadershipPeoplePage, self).get_context(request)
        context["ourpeoplepage"] = OurPeoplePage.objects.filter(
            slug="our-people"
        ).first()

        return context

    class Meta:
        verbose_name = "Our Staff and Leadership Page"
