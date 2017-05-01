from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey


class AbstractProgram(Page):
    """
    Abstract Program class that inherits from Page and is inherited
    by Program and Subprogram models
    """
    name = models.CharField(max_length=100, help_text='Name of Program')
    location = models.NullBooleanField(
        help_text='Select if location based program i.e. New America NYC'
    )
    description = models.TextField()

    # Up to four lead stories can be featured on the homepage.
    # Lead_1 will be featured most prominently.
    lead_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_4 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Up to three featured stories to appear underneath
    # the lead stories. All of the same size and formatting.
    feature_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    featured_stories = [feature_1, feature_2, feature_3]

    # Carousel of pages to feature on the landing page
    feature_carousel = StreamField([
        ('page', PageChooserBlock()),
    ], blank=True)

    about_us_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Story excerpt and story image fields are to provide information
    # about the program or subprogram if they are featured on a homepage
    # or program landing page
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
        MultiFieldPanel(
            [
                PageChooserPanel('lead_1'),
                PageChooserPanel('lead_2'),
                PageChooserPanel('lead_3'),
                PageChooserPanel('lead_4'),
            ],
            heading="Lead Stories",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel('feature_1'),
                PageChooserPanel('feature_2'),
                PageChooserPanel('feature_3'),
            ],
            heading="Featured Stories",
            classname="collapsible"
        ),
        StreamFieldPanel('feature_carousel'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name', classname='full title'),
        FieldPanel('location'),
        FieldPanel('description'),
        PageChooserPanel('about_us_page', 'home.ProgramSimplePage'),
    ]

    def get_context(self, request):
        context = super(AbstractProgram, self).get_context(request)

        # In order to apply different styling to main lead story
        # versus the other lead stories, we needed to separate them out
        context['other_lead_stories'] = []

        # Solution to account for null values for the stories
        # so that the div in the template wouldn't attempt to add styling to nothing
        if self.lead_2:
            context['other_lead_stories'].append(self.lead_2)
        if self.lead_3:
            context['other_lead_stories'].append(self.lead_3)
        if self.lead_4:
            context['other_lead_stories'].append(self.lead_4)

        # In order to preserve style, minimum and maximum of feature stories is 3
        # If there are less than 3 feature stories - none show up even if they're added.
        if self.feature_1 and self.feature_2 and self.feature_3:
            context['featured_stories'] = [
                self.feature_1, self.feature_2, self.feature_3
            ]
        else:
            context['featured_stories'] = []

        return context

    def get_experts(self):
        """
        Method for the Program and Subprogram models to be able to access
        people from Person model who have been marked as experts
        """
        return self.person_set.filter(expert=True).order_by('-title')

    def get_subprograms(self):
        """
        Method that returns the subprograms that live underneath
        a particular program
        """
        return self.get_children().type(Subprogram).live().in_menu()

    class Meta:
        abstract = True


class Program(AbstractProgram):
    """
    Program model which creates the parent program pages
    that live under the homepage.
    """
    parent_page_types = ['home.HomePage']
    subpage_types = [
    'article.ProgramArticlesPage',
    'book.ProgramBooksPage',
    'blog.ProgramBlogPostsPage',
    'event.ProgramEventsPage',
    'podcast.ProgramPodcastsPage',
    'policy_paper.ProgramPolicyPapersPage',
    'press_release.ProgramPressReleasesPage',
    'quoted.ProgramQuotedPage',
    'home.ProgramSimplePage',
    'person.ProgramPeoplePage',
    'Subprogram',
    'issue.IssueOrTopic',
    'home.RedirectPage',
    ]

    desktop_program_logo = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    mobile_program_logo = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    sidebar_menu_initiatives_and_projects_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    sidebar_menu_our_work_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    sidebar_menu_about_us_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    content_panels = AbstractProgram.content_panels + [
        ImageChooserPanel('desktop_program_logo'),
        ImageChooserPanel('mobile_program_logo'),
    ]

    promote_panels = AbstractProgram.promote_panels + [
        StreamFieldPanel('sidebar_menu_about_us_pages'),
        StreamFieldPanel('sidebar_menu_initiatives_and_projects_pages'),
        StreamFieldPanel('sidebar_menu_our_work_pages'),
    ]

    def get_context(self, request):
        context = super(Program, self).get_context(request)

        return context

    class Meta:
        ordering = ('title',)


# Through relationship for Programs to Subprogram
class ProgramSubprogramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    subprogram = ParentalKey('Subprogram', related_name='programs')
    panels = [
        FieldPanel('program'),
    ]


class Subprogram(AbstractProgram):
    """
    Subprograms model which can be created under programs and
    also be connected to multiple programs. Can also create content homepages
    underneath subprograms in the same way they can be created under programs.
    """
    parent_page_types = ['programs.Program']
    subpage_types = [
    'article.ProgramArticlesPage',
    'book.ProgramBooksPage',
    'blog.ProgramBlogPostsPage',
    'event.ProgramEventsPage',
    'podcast.ProgramPodcastsPage',
    'policy_paper.ProgramPolicyPapersPage',
    'press_release.ProgramPressReleasesPage',
    'quoted.ProgramQuotedPage',
    'home.ProgramSimplePage',
    'person.ProgramPeoplePage',
    'issue.IssueOrTopic',
    'home.RedirectPage',
    ]

    parent_programs = models.ManyToManyField(
        Program,
        through=ProgramSubprogramRelationship,
        blank=True
    )
    content_panels = AbstractProgram.content_panels + [
        InlinePanel('programs', label=("Programs")),
    ]

    def get_template(self, request):
        return 'programs/program.html'

    class Meta:
        verbose_name = "Subprogram/Initiative Page"
        ordering = ('title',)

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program relationship is
        captured even if the user does not select it
        """
        super(Subprogram, self).save(*args, **kwargs)
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(
            slug=program_title.slug
        )

        if isinstance(program, AbstractProgram):
            relationship, created=ProgramSubprogramRelationship.objects.get_or_create(
                program=program,
                subprogram=self
            )
            if created:
                relationship.save()

class ProgramContentHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Content associated with a specific program or Subprogram
    """
    parent_program = models.ForeignKey(Program, on_delete=models.SET_NULL, blank=True, null=True)
    parent_subprogram = models.ForeignKey(Subprogram, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self,*args,**kwargs):
        super(ProgramContentHomePage, self).save(*args,**kwargs)
        program = self.get_ancestors()[2]
        if isinstance(program, Program):
            self.parent_program = program
        elif isinstance(program, Subprogram):
            self.parent_subprogram = program

        self.save()
