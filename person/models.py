from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.wagtailcore.blocks import URLBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel, MultiFieldPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

from programs.models import Program, Subprogram

from newamericadotorg.helpers import paginate_results

from django.db.models import Q


# Through relationship that connects the Person model
# to the Program model so that a Person may belong
# to more than one Program
class PersonProgramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    person = ParentalKey('Person', related_name='programs')
    panels = [
        FieldPanel('program'),
    ]


# Through relationship that connects the Person model
# to the Subprogram model so that a Person may belong
# to more than one Subprogram
class PersonSubprogramRelationship(models.Model):
    subprogram = models.ForeignKey(Subprogram, related_name="+")
    person = ParentalKey('Person', related_name='subprograms')
    panels = [
        FieldPanel('subprogram'),
    ]


class Person(Page):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    position_at_new_america = models.CharField(
        max_length=500,
        help_text="Position or Title at New America",
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True, null=True)
    short_bio = RichTextField(blank=True, null=True)
    long_bio = RichTextField(blank=True, null=True)
    expert = models.BooleanField(default=False)
    leadership = models.BooleanField(default=False)
    profile_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    belongs_to_these_programs = models.ManyToManyField(
        Program,
        through=PersonProgramRelationship,
        blank=True
    )

    belongs_to_these_subprograms = models.ManyToManyField(
        Subprogram,
        through=PersonSubprogramRelationship,
        blank=True,
    )

    social_media = StreamField([
        ('twitter',
            URLBlock(
                required=False,
                help_text='Twitter Profile Link',
                icon='user'
            )),
        ('facebook',
            URLBlock(
                required=False,
                help_text='Facebook Profile',
                icon='user'
            )),
        ('youtube',
            URLBlock(
                required=False,
                help_text='YouTube Channel',
                icon='media'
            )),
        ('google_plus',
            URLBlock(
                required=False,
                help_text='Google+ Profile',
                icon='user'
            )),
        ('linkedin',
            URLBlock(
                required=False,
                help_text='LinkedIn Profile',
                icon='user'
            )),
        ('tumblr',
            URLBlock(
                required=False,
                help_text='Tumblr',
                icon='user'
            )),
    ])

    ROLE_OPTIONS = (
        ('Board Chair', 'Board Chair'),
        ('Board Member', 'Board Member'),
        ('Fellow', 'Fellow'),
        ('Central Staff', 'Central Staff'),
        ('Program Staff', 'Program Staff'),
        ('External Author/Former Staff', 'External Author')
    )
    role = models.CharField(choices=ROLE_OPTIONS, max_length=50)
    former = models.BooleanField(default=False, help_text="Select if person no longer serves above role.")

    # Up to three featured work pages to appear on bio page
    feature_work_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_work_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_work_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
            ImageChooserPanel('profile_image'),
            FieldPanel('short_bio'),
            FieldPanel('long_bio', classname="full")
        ], heading="About"),

        MultiFieldPanel([
            FieldPanel('position_at_new_america'),
                FieldPanel('role'),
                FieldPanel('former'),
                FieldPanel('expert'),
                FieldPanel('leadership')
        ], heading="Role"),

        InlinePanel('programs',
            label=("Belongs to these Programs")),
        InlinePanel('subprograms', label=("Belongs to these Subprograms/Initiatives")),
        InlinePanel('topics', label="Expert in these topics"),

        MultiFieldPanel([
            FieldPanel('email'),
            StreamFieldPanel('social_media')
        ], heading="Contact"),


        MultiFieldPanel([
            PageChooserPanel(
                'feature_work_1',
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle']),
            PageChooserPanel(
                'feature_work_2',
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle']),
            PageChooserPanel(
                'feature_work_3',
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle']),
        ], heading="Featured Work To Highlight on Bio Page", classname="collapsible"),
    ]

    parent_page_types = ['OurPeoplePage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('position_at_new_america'),
        index.SearchField('long_bio'),
        index.SearchField('short_bio'),
        index.SearchField('role'),

        index.RelatedFields('belongs_to_these_programs', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('belongs_to_these_subprograms', [
            index.SearchField('name'),
        ]),
    ]

    def get_context(self, request):
        context = super(Person, self).get_context(request)
        featured_work = [
            self.feature_work_1,
            self.feature_work_2,
            self.feature_work_3
        ]

        context['featured_work'] = featured_work

        # Returns posts that the person has authored ordered by date
        context['posts'] = paginate_results(request, self.post_set.live().order_by("-date"))

        return context

    class Meta:
        ordering = ('last_name',)


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns everyone from the Person model
    """
    parent_page_types = ['home.HomePage']
    subpage_types = ['Person']

    page_description = RichTextField(blank=True, null=True)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('story_image'),
    ]

    def get_context(self, request):
        context = super(OurPeoplePage, self).get_context(request)

        context['people'] = Person.objects.live().filter(former=False).exclude(
            role='External Author/Former Staff')

        context['all_programs'] = Program.objects.live()

        context['all_our_people_pages'] = ProgramPeoplePage.objects.live()

        return context

    class Meta:
        verbose_name = "Homepage for All People in NAF"


class ExpertPage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone who is marked as an expert from the Person model
    """
    parent_page_types = ['home.HomePage']
    subpage_types = []

    page_description = RichTextField(blank=True, null=True)
    contact_information = RichTextField(blank=True, null=True)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('contact_information'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('story_image'),
    ]

    def get_context(self, request):
        context = super(ExpertPage, self).get_context(request)

        context['non_program_experts'] = Person.objects\
            .live()\
            .filter(belongs_to_these_programs=None)\
            .filter(expert=True)\
            .order_by('-title')

        context['all_programs'] = Program.objects.live()

        context['all_our_people_pages'] = ProgramPeoplePage.objects.live()

        return context


class ProgramPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = []

    def get_context(self, request):
        context = super(ProgramPeoplePage, self).get_context(request)

        if self.depth == 4:
            program_title = self.get_ancestors()[2]
            program = Program.objects.get(title=program_title)
            all_posts = Person.objects\
                .live()\
                .filter(belongs_to_these_programs=program, former=False)\
                .exclude(role__icontains='External Author')\
                .order_by('last_name', 'first_name')
        else:
            subprogram_title = self.get_ancestors()[3]
            program = Subprogram.objects.get(title=subprogram_title)
            all_posts = Person.objects\
                .live()\
                .filter(belongs_to_these_subprograms=program, former=False)\
                .exclude(role__icontains='External Author')\
                .order_by('last_name', 'first_name')

        context['people'] = paginate_results(request, all_posts)

        context['program'] = program

        return context

    class Meta:
        verbose_name = "Our People Page for Programs and Subprograms"


class BoardAndLeadershipPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """
    parent_page_types = ['home.HomePage']
    subpage_types = []

    page_description = RichTextField(blank=True, null=True)

    QUERY_OPTIONS = (
        ('Board Member', 'Board Members'),
        ('Leadership Team', 'Leadership Team'),
        ('Central Staff', 'Central Staff'),
    )
    role_query = models.CharField(choices=QUERY_OPTIONS, max_length=50, default='Board Members')
    former_query = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('role_query'),
        FieldPanel('former_query')
    ]

    def get_context(self, request):
        context = super(BoardAndLeadershipPeoplePage, self).get_context(request)

        which_role = self.role_query
        is_former = self.former_query

        all_people = Person.objects.live()\
            .filter(former=is_former)\
            .order_by('last_name', 'first_name')

        if which_role == 'Leadership Team':
            all_people = all_people.filter(leadership=True)
        elif which_role == 'Board Member':
            all_people = all_people.filter(Q(role=which_role) | Q(role='Board Chair')).order_by('role', 'last_name')
        else:
            all_people = all_people.filter(role=which_role)


        context['people'] = paginate_results(request, all_people)

        return context

    class Meta:
        verbose_name = "Our People Page for Board of Directors, Central Staff, and Leadership Team"
