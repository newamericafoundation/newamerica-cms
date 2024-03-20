from django import forms
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from multiselectfield import MultiSelectField
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
    TitleFieldPanel,
)
from wagtail.blocks import StreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtailautocomplete.edit_handlers import AutocompletePanel

from home.models import Post
from person.models import Person
from programs.models import AbstractContentPage

from .blocks import CtaBlock
from .utils import DATA_TYPE_CHOICES, MONTH_CHOICES


class PageAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Survey Home Page and Authors
    """

    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="+")
    page = ParentalKey("SurveysHomePage", related_name="authors")

    panels = [
        FieldPanel("author"),
    ]

    class Meta:
        ordering = ["pk"]


class SurveysHomePage(AbstractContentPage):
    parent_page_types = ["programs.Program", "programs.Subprogram", "programs.Project"]
    subpage_types = ["Survey", "SurveyValuesIndex"]

    partner_logo = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    partner_logo_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Partner logo alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )
    about = RichTextField(
        max_length=1500, blank=True, verbose_name="About This Project"
    )
    page_author = models.ManyToManyField(
        Person, through=PageAuthorRelationship, blank=True
    )
    subscribe = StreamField(
        StreamBlock([("cta_block", CtaBlock())], max_num=1, required=False),
        use_json_field=True,
        null=True,
        blank=True,
    )
    submissions = StreamField(
        StreamBlock([("cta_block", CtaBlock())], max_num=1, required=False),
        null=True,
        blank=True,
        use_json_field=True,
    )
    about_submission = RichTextField(max_length=500, blank=True)
    subheading = models.CharField(max_length=300, blank=True)
    methodology = RichTextField(max_length=1500, blank=True)
    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("subheading"),
        MultiFieldPanel(
            [
                FieldPanel("subscribe"),
                FieldPanel("submissions"),
            ],
            heading="Survey Reports CTAs",
        ),
    ]
    about_panels = [
        MultiFieldPanel(
            [
                FieldPanel("about"),
                FieldPanel("methodology"),
                FieldPanel("about_submission"),
                InlinePanel("authors", label="Authors"),
                FieldPanel("partner_logo"),
                FieldPanel("partner_logo_alt"),
            ],
            heading="About Tab",
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Survey Reports Tab"),
            ObjectList(about_panels, heading="About Tab"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request):
        context = super(SurveysHomePage, self).get_context(request)
        context["authors"] = self.authors.order_by("pk")

        return context

    def save(self, *args, **kwargs):
        super(SurveysHomePage, self).save(*args, **kwargs)
        if self.get_children_count() == 0:
            self.add_child(
                instance=SurveyValuesIndex(
                    title=self.title + " Filters", slug=slugify(self.title + " Filters")
                )
            )

    @property
    def content_model(self):
        return SurveysHomePage

    class Meta:
        verbose_name = "Survey Database"

    def __str__(self):
        return self.title


class SurveyOrganization(Page):
    parent_page_types = ["SurveyValuesIndex"]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Survey Organizations"


class DemographicKey(Page):
    parent_page_types = ["SurveyValuesIndex"]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Demographic Keys"


class SurveyTags(Page):
    parent_page_types = ["SurveyValuesIndex"]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Survey Tags"


# SurveyValuesIndex page is the parent page for a SurveyHomePage's associated filters.
# (ex. Demographics, Tags, Organizations). These values can be created and edited here.
# Everytime a SurveyHomePage is created a child SurveyValuesIndex page is generated and adopts its title.
# (ex. the surveyhomepage 'Magic Survey', will generate a child values index page 'Magic Survey Filters')


class SurveyValuesIndex(Page):
    parent_page_types = ["SurveysHomePage"]
    subpage_type = ["SurveyOrganization", "DemographicKey", "SurveyTags"]

    class Meta:
        verbose_name = "Survey Filters Parent"

    def __str__(self):
        return self.title


class Survey(Post):
    template = "survey/survey.html"
    parent_page_types = ["SurveysHomePage"]

    description = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        help_text="A brief description of the survey. 500 chars max",
    )
    org = ParentalManyToManyField(
        "SurveyOrganization",
        related_name="SurveyOrganization",
        blank=True,
        verbose_name="Organization",
    )
    year = models.IntegerField(
        help_text="Year Survey was conducted.", blank=True, default=2000
    )
    month = models.CharField(
        choices=MONTH_CHOICES,
        default=None,
        help_text="Month Survey was conducted, if applicable.",
        max_length=3,
        blank=True,
        null=True,
    )
    sample_number = models.IntegerField(blank=True, null=True)
    demos_key = ParentalManyToManyField(
        "DemographicKey",
        help_text="Indexable demographic groups",
        blank=True,
        default=False,
        verbose_name="Demographics Keys",
    )
    findings = RichTextField(blank=True, null=True, max_length=12500)
    data_type = MultiSelectField(choices=DATA_TYPE_CHOICES)
    national = models.BooleanField(
        default=True,
        verbose_name="Nationally Representative?",
        help_text="Indicates whether the survey was nationally representative or not.",
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Link to Survey",
        help_text="Add a link to a webpage containing the survey details.",
    )
    file = models.FileField(
        blank=True,
        null=True,
        verbose_name="Survey File",
        help_text="Add a file containing the survey details.",
    )
    tags = ParentalManyToManyField(
        "SurveyTags",
        help_text="Select from available tags",
        blank=True,
        default=False,
        verbose_name="Topics",
    )
    content_panels = [
        MultiFieldPanel(
            [
                TitleFieldPanel("title"),
                FieldPanel("date"),
            ],
            heading="Survey Created",
        ),
        MultiFieldPanel(
            [
                FieldPanel("description"),
                AutocompletePanel("org"),
                FieldPanel("year"),
                FieldPanel("month"),
                FieldPanel("sample_number"),
                AutocompletePanel("demos_key"),
                AutocompletePanel("tags"),
                FieldPanel("data_type", widget=forms.CheckboxSelectMultiple),
                FieldPanel("national"),
                FieldPanel("findings"),
                InlinePanel("associated_commentary", label="Associated Commentary"),
            ],
            heading="Survey Data",
        ),
        MultiFieldPanel([FieldPanel("link"), FieldPanel("file")]),
    ]

    class Meta:
        verbose_name = "Survey"

    def __str__(self):
        return self.title


class AssociatedCommentary(Orderable):
    commentary = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+")
    survey = ParentalKey("Survey", related_name="associated_commentary")

    panels = [
        FieldPanel("commentary"),
    ]
