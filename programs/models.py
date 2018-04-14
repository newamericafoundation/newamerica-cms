from django.db import models
from wagtail.wagtailadmin.edit_handlers import TabbedInterface, ObjectList
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailcore.blocks import PageChooserBlock, ChoiceBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from subscribe.models import SubscriptionSegment
from modelcluster.fields import ParentalKey
from newamericadotorg.blocks import BodyBlock

class SubscriptionProgramRelationship(models.Model):
    subscription_segment = models.ForeignKey(SubscriptionSegment, related_name="+")
    program = ParentalKey('Program', related_name='subscriptions')
    alternate_title = models.TextField(blank=True)
    panels = [
        FieldPanel('subscription_segment'),
        FieldPanel('alternate_title')
    ]

class SubscriptionSubprogramRelationship(models.Model):
    subscription_segment = models.ForeignKey(SubscriptionSegment, related_name="+")
    subprogram = ParentalKey('Subprogram', related_name='subscriptions')
    alternate_name = models.TextField(blank=True)
    panels = [
        FieldPanel('subscription_segment'),
        FieldPanel('alternate_name')
    ]


class AbstractProgram(Page):
    """
    Abstract Program class that inherits from Page and is inherited
    by Program and Subprogram models
    """
    name = models.CharField(max_length=100, help_text='Name of Program')
    fellowship = models.NullBooleanField(
        help_text='Select if this is a fellowship program'
    )
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

    featured_panels = [
        MultiFieldPanel(
            [
                PageChooserPanel('lead_1'),
                PageChooserPanel('lead_2'),
                PageChooserPanel('lead_3'),
                PageChooserPanel('lead_4'),
                PageChooserPanel('feature_1'),
                PageChooserPanel('feature_2'),
                PageChooserPanel('feature_3')
            ],
            heading="Lead Stories",
            classname="collapsible"
        ),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('name', classname='full title'),
                ImageChooserPanel('story_image'),
                PageChooserPanel('about_us_page', 'home.ProgramSimplePage'),
                FieldPanel('location'),
                FieldPanel('fellowship'),
                FieldPanel('description'),
                FieldPanel('story_excerpt'),
            ],
            heading="Setup",
            classname="collapsible"
        ),
    ]

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
    'Project',
    'BlogProject',
    'issue.TopicHomepage',
    'home.RedirectPage',
    'report.ReportsHomepage',
    'PublicationsPage',
    'other_content.ProgramOtherPostsPage'
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

    subscription_segments = models.ManyToManyField(
        SubscriptionSegment,
        through=SubscriptionProgramRelationship,
        blank=True,
    )

    content_panels = AbstractProgram.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('desktop_program_logo'),
            ImageChooserPanel('mobile_program_logo'),
        ], heading="Logos")
    ]

    promote_panels = AbstractProgram.promote_panels + [
        InlinePanel('subscriptions', label=("Subscription Segments")),
    ]

    sidebar_panels = [
        StreamFieldPanel('sidebar_menu_about_us_pages'),
        # StreamFieldPanel('sidebar_menu_initiatives_and_projects_pages'),
        # StreamFieldPanel('sidebar_menu_our_work_pages'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading="Content"),
        ObjectList(AbstractProgram.featured_panels, heading="Featured"),
        ObjectList(promote_panels, heading="Promote"),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
        ObjectList(sidebar_panels, heading="Sidebar")
    ])

    class Meta:
        ordering = ('title',)
        verbose_name = 'Program Homepage'


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
    'report.ReportsHomepage',
    'policy_paper.ProgramPolicyPapersPage',
    'press_release.ProgramPressReleasesPage',
    'quoted.ProgramQuotedPage',
    'home.ProgramSimplePage',
    'person.ProgramPeoplePage',
    'issue.IssueOrTopic',
    'home.RedirectPage',
    'PublicationsPage',
    'other_content.ProgramOtherPostsPage'
    ]

    TEMPLATE_OPTIONS =  (
        ('programs/program.html', 'Full'),
        ('simple_program.html', 'Efficiency'),
        ('programs/program.html', 'Collection')
    )

    template = models.CharField(choices=TEMPLATE_OPTIONS, default='programs/program.html', max_length=100)

    parent_programs = models.ManyToManyField(
        Program,
        through=ProgramSubprogramRelationship,
        blank=True
    )

    subscription_segments = models.ManyToManyField(
        SubscriptionSegment,
        through=SubscriptionSubprogramRelationship,
        blank=True,
    )

    content_panels = [ FieldPanel('template') ] + AbstractProgram.content_panels + [
        InlinePanel('programs', label=("Programs")),
    ]

    promote_panels = AbstractProgram.promote_panels + [
        InlinePanel('subscriptions', label=("Subscription Segments")),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(AbstractProgram.featured_panels, heading='Featured'),
        ObjectList(promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def get_template(self, request):
        return 'programs/program.html'

    class Meta:
        verbose_name = 'Initiative/Project Homepage'
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

class BlogSeries(Page):
    parent_page_types = ['BlogProject']
    subpage_types = [
    'article.Article',
    'book.Book',
    'blog.BlogPost',
    'podcast.Podcast',
    'quoted.Quoted',
    ]

class Project(Subprogram):
    redirect_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Select a report or other post that you would like to show up as a project in your Initiatives & Projects list'
    )

    content_panels = [
        PageChooserPanel('redirect_page')
    ] + Subprogram.content_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Subprogram.featured_panels, heading='Featured'),
        ObjectList(Subprogram.promote_panels, heading='Promote'),
        ObjectList(Subprogram.settings_panels, heading='Settings', classname='settings'),
    ])

class BlogProject(Subprogram):
    subpage_types = [
    'article.Article',
    'book.Book',
    'blog.BlogPost',
    'podcast.Podcast',
    'quoted.Quoted',
    'BlogSeries'
    ]
    class Meta:
        verbose_name = 'Blog'

class AbstractContentPage(Page):
    """
    Convenience Class for querying all Content homepages
    """

    def get_context(self, request):
        context = super(AbstractContentPage, self).get_context(request)
        context['program'] = self.get_parent().specific

        return context

    class Meta:
        abstract=True

class PublicationsPage(AbstractContentPage):
    '''
    '''
    parent_page_types = ['home.HomePage', 'Program', 'Subprogram']

    def get_template(self, request):
        parent = self.get_parent()
        if parent.content_type.model == 'program':
            return 'programs/publications_page.html'
        return 'home/publications_page.html'

    class Meta:
        verbose_name = 'Publications Homepage'
