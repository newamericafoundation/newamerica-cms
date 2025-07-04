import json

from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.blocks import PageChooserBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

from subscribe.models import SubscribePageSegmentPlacement


class FeaturedProgramPage(Orderable):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="+")
    program = ParentalKey("Program", related_name="featured_pages")
    featured_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Featured image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    panels = [
        FieldPanel("page"),
        FieldPanel("featured_image"),
        FieldPanel("featured_image_alt"),
    ]


class FeaturedSubprogramPage(Orderable):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="+")
    program = ParentalKey("Subprogram", related_name="featured_pages")
    featured_image = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    featured_image_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Featured image alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    panels = [
        FieldPanel("page"),
        FieldPanel("featured_image"),
        FieldPanel("featured_image_alt"),
    ]

@register_snippet
class ProgramNavOptions(models.Model):
    description = models.TextField(
        help_text="Human-readable description for these options to show when listing in the Wagtail admin.",
    )
    url_label_array = models.TextField(
        help_text='Must contain an array of objects formatted as JSON text.  Example: [{"url": "about/", "label": "About Page"}, {"url": "our-people/", "label": "All Our People"}]',
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Program Nav Options"


class AbstractProgram(RoutablePageMixin, Page):
    """
    Abstract Program class that inherits from Page and is inherited
    by Program and Subprogram models
    """

    name = models.CharField(max_length=100, help_text="Name of Program")
    former = models.BooleanField(
        default=False, help_text="Select if no longer active"
    )
    fellowship = models.BooleanField(
        null=True,
        blank=True,
        help_text="Select if this is a fellowship program",
    )
    location = models.BooleanField(
        null=True,
        blank=True,
        help_text="Select if location based program i.e. New America NYC",
    )
    description = models.TextField()

    # Story excerpt and story image fields are to provide information
    # about the program or subprogram if they are featured on a homepage
    # or program landing page
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)

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

    hide_subscription_card = models.BooleanField(default=False)
    subscription_card_text = models.TextField(
        blank=True, null=True, max_length=100
    )

    nav_options = models.ForeignKey(
        ProgramNavOptions,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    featured_panels = [
        InlinePanel(
            "featured_pages",
            label="Featured Pages",
            help_text="CHANGED MARCH 2023: Pages are shown in reverse order. The last page in this list is shown as the lead story.",
        )
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("name", classname="full title"),
                FieldPanel("story_image"),
                FieldPanel("story_image_alt"),
                FieldPanel("location"),
                FieldPanel("fellowship"),
                FieldPanel("description"),
                FieldPanel("story_excerpt"),
                FieldPanel("former"),
            ],
            heading="Setup",
            classname="collapsible",
        ),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("nav_options"),
    ]

    def get_experts(self):
        """
        Method for the Program and Subprogram models to be able to access
        people from Person model who have been marked as experts
        """
        return self.person_set.filter(expert=True).order_by("-title")

    def get_subscription_segments(self):
        return SubscribePageSegmentPlacement.objects.children_of(self)

    def get_subprograms(self):
        """
        Method that returns the subprograms that live underneath
        a particular program
        """
        return self.get_children().type(Subprogram).live().in_menu()

    @route(
        r"^(?:our-people|events|projects|publications|topics|about|subscribe)/$"
    )
    def program_subpage(self, request):
        return self.render(request)

    class Meta:
        abstract = True


class Program(AbstractProgram):
    """
    Program model which creates the parent program pages
    that live under the homepage.
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "article.ProgramArticlesPage",
        "book.ProgramBooksPage",
        "blog.ProgramBlogPostsPage",
        "event.ProgramEventsPage",
        "podcast.ProgramPodcastsPage",
        "policy_paper.ProgramPolicyPapersPage",
        "brief.ProgramBriefsPage",
        "press_release.ProgramPressReleasesPage",
        "quoted.ProgramQuotedPage",
        "home.ProgramSimplePage",
        "person.ProgramPeoplePage",
        "Subprogram",
        "Project",
        "issue.TopicHomepage",
        "home.RedirectPage",
        "report.ReportsHomepage",
        "PublicationsPage",
        "other_content.ProgramOtherPostsPage",
        "home.ProgramAboutHomePage",
        "survey.SurveysHomePage",
        "home.SubscribePage",
    ]

    desktop_program_logo = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    desktop_program_logo_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Desktop program logo alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    mobile_program_logo = models.ForeignKey(
        "home.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    mobile_program_logo_alt = models.TextField(
        default="",
        blank=True,
        verbose_name="Mobile program logo alternative text",
        help_text="A concise description of the image for users of assistive technology.",
    )

    display_logo_as_name = models.BooleanField(
        default=False,
        verbose_name="Display program logo instead of text program name",
    )

    sidebar_menu_about_us_pages = StreamField(
        [
            ("Item", PageChooserBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = AbstractProgram.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("desktop_program_logo"),
                FieldPanel("desktop_program_logo_alt"),
                FieldPanel("mobile_program_logo"),
                FieldPanel("mobile_program_logo_alt"),
            ],
            heading="Logos",
        )
    ]

    promote_panels = AbstractProgram.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hide_subscription_card"),
                FieldPanel("subscription_card_text"),
                FieldPanel("display_logo_as_name"),
            ]
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(AbstractProgram.featured_panels, heading="Featured"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(
                Page.settings_panels, heading="Settings", classname="settings"
            ),
        ]
    )

    def get_context(self, request):
        context = super().get_context(request)

        if getattr(request, "is_preview", False):
            import newamericadotorg.api
            from issue.models import IssueOrTopic

            revision = self.get_latest_revision_as_object()
            topics = IssueOrTopic.objects.live().filter(
                depth=5, parent_program__id=self.id
            )
            topics = [t.get_latest_revision_as_object() for t in topics]
            program_data = newamericadotorg.api.program.serializers.ProgramDetailSerializer(
                revision, context={"is_preview": True}
            ).data
            topic_data = (
                newamericadotorg.api.topic.serializers.TopicSerializer(
                    topics, many=True
                ).data
            )
            context["initial_state"] = json.dumps(program_data)
            context["initial_topics_state"] = json.dumps(topic_data)

        return context

    class Meta:
        ordering = ("title",)
        verbose_name = "Program Homepage"


# Through relationship for Programs to Subprogram
class ProgramSubprogramRelationship(models.Model):
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name="+"
    )
    subprogram = ParentalKey("Subprogram", related_name="programs")
    panels = [
        FieldPanel("program"),
    ]


class Subprogram(AbstractProgram):
    """
    Subprograms model which can be created under programs and
    also be connected to multiple programs. Can also create content homepages
    underneath subprograms in the same way they can be created under programs.
    """

    parent_page_types = ["programs.Program"]
    subpage_types = [
        "article.ProgramArticlesPage",
        "book.ProgramBooksPage",
        "blog.ProgramBlogPostsPage",
        "event.ProgramEventsPage",
        "podcast.ProgramPodcastsPage",
        "report.ReportsHomepage",
        "policy_paper.ProgramPolicyPapersPage",
        "brief.ProgramBriefsPage",
        "press_release.ProgramPressReleasesPage",
        "quoted.ProgramQuotedPage",
        "home.ProgramSimplePage",
        "person.ProgramPeoplePage",
        "issue.IssueOrTopic",
        "home.RedirectPage",
        "PublicationsPage",
        "other_content.ProgramOtherPostsPage",
        "home.ProgramAboutHomePage",
        "survey.SurveysHomePage",
        "home.SubscribePage",
    ]

    TEMPLATE_OPTIONS = (
        ("programs/program.html", "Full"),
        ("simple_program.html", "Efficiency"),
        ("programs/program.html", "Collection"),
    )

    template = models.CharField(
        choices=TEMPLATE_OPTIONS,
        default="programs/program.html",
        max_length=100,
    )

    parent_programs = models.ManyToManyField(
        Program, through=ProgramSubprogramRelationship, blank=True
    )

    content_panels = (
        [FieldPanel("template")]
        + AbstractProgram.content_panels
        + [
            InlinePanel("programs", label=("Programs")),
        ]
    )

    promote_panels = AbstractProgram.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hide_subscription_card"),
                FieldPanel("subscription_card_text"),
            ]
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(AbstractProgram.featured_panels, heading="Featured"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(
                Page.settings_panels, heading="Settings", classname="settings"
            ),
        ]
    )

    def get_template(self, request):
        return "programs/program.html"

    def get_context(self, request):
        context = super().get_context(request)
        if getattr(request, "is_preview", False):
            import newamericadotorg.api

            revision = self.get_latest_revision_as_object()
            program_data = (
                newamericadotorg.api.program.serializers.SubprogramSerializer(
                    revision, context={"is_preview": True}
                ).data
            )
            context["initial_state"] = json.dumps(program_data)
            context["initial_topics_state"] = None

        return context

    class Meta:
        verbose_name = "Initiative Homepage"
        ordering = ("title",)

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program relationship is
        captured even if the user does not select it
        """
        super(Subprogram, self).save(*args, **kwargs)
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(slug=program_title.slug)

        if isinstance(program, AbstractProgram):
            (
                relationship,
                created,
            ) = ProgramSubprogramRelationship.objects.get_or_create(
                program=program, subprogram=self
            )
            if created:
                relationship.save()


class Project(Subprogram):
    parent_page_types = ["programs.Program"]
    subpage_types = [
        "article.ProgramArticlesPage",
        "book.ProgramBooksPage",
        "blog.ProgramBlogPostsPage",
        "event.ProgramEventsPage",
        "podcast.ProgramPodcastsPage",
        "report.ReportsHomepage",
        "policy_paper.ProgramPolicyPapersPage",
        "brief.ProgramBriefsPage",
        "press_release.ProgramPressReleasesPage",
        "quoted.ProgramQuotedPage",
        "home.ProgramSimplePage",
        "person.ProgramPeoplePage",
        "issue.IssueOrTopic",
        "home.RedirectPage",
        "PublicationsPage",
        "other_content.ProgramOtherPostsPage",
        "home.ProgramAboutHomePage",
        "survey.SurveysHomePage",
    ]

    redirect_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Select a report or other post that you would like to show up as a project in your Initiatives & Projects list",
    )

    content_panels = [FieldPanel("redirect_page")] + Subprogram.content_panels

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(Subprogram.featured_panels, heading="Featured"),
            ObjectList(Subprogram.promote_panels, heading="Promote"),
            ObjectList(
                Subprogram.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    @classmethod
    def get_indexed_objects(cls):
        # do not add projects with a redirect page to the search index
        return cls.objects.filter(redirect_page__isnull=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "Project"

    @route(r"^$")
    @route(
        r"^(our-people|events|projects|publications|topics|about|subscribe)/$"
    )
    def redirect_to_subprogram(self, request, section=""):
        redirect_page = getattr(self, "redirect_page", None)
        if redirect_page:
            if isinstance(redirect_page.specific, Subprogram) and section:
                return redirect(redirect_page.url + section + "/")
            return HttpResponseRedirect(redirect_page.url)
        return self.render(request)


class AbstractContentPage(Page):
    """
    Convenience Class for querying all Content homepages
    """

    def get_context(self, request):
        context = super(AbstractContentPage, self).get_context(request)
        context["program"] = self.get_parent().specific

        return context

    class Meta:
        abstract = True


class PublicationsPage(AbstractContentPage):
    """ """

    parent_page_types = ["home.HomePage", "Program", "Subprogram", "Project"]

    def get_template(self, request):
        parent = self.get_parent()
        if issubclass(parent.specific_class, Program):
            return "programs/publications_page.html"
        return "home/publications_page.html"

    class Meta:
        verbose_name = "Publications Homepage"
