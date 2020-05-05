from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.core.blocks import URLBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import PageChooserPanel, MultiFieldPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey

from programs.models import Program, Subprogram, AbstractContentPage

from newamericadotorg.helpers import paginate_results

from django.db.models import Q
import datetime

ROLE_OPTIONS = (
    ('Board Chair', 'Board Chair'),
    ('Board Member', 'Board Member'),
    ('Fellow', 'Fellow'),
    ('Central Staff', 'Central Staff'),
    ('Program Staff', 'Program Staff'),
    ('External Author/Former Staff', 'External Author')
)
GROUPING_OPTIONS = (
    ('Current Fellows', 'Current Fellows'),
    ('Former Fellows', 'Former Fellows'),
    ('Advisors', 'Advisors'),
    ('Contributing Staff', 'Contributing Staff')
)
YEAR_CHOICES = [(r,r) for r in range(1999, datetime.date.today().year+1)]
YEAR_CHOICES.reverse()

# Through relationship that connects the Person model
# to the Program model so that a Person may belong
# to more than one Program
class PersonProgramRelationship(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="+")
    person = ParentalKey('Person', related_name='programs')
    group = models.CharField(choices=GROUPING_OPTIONS, max_length=50, blank=True, null=True, help_text='Set grouping for program\'s our people page')
    fellowship_position = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Set program-specific fellowship information"
    )
    fellowship_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    panels = [
        FieldPanel('program'),
        FieldPanel('group'),
        FieldPanel('fellowship_position'),
        FieldPanel('fellowship_year')
    ]


# Through relationship that connects the Person model
# to the Subprogram model so that a Person may belong
# to more than one Subprogram
class PersonSubprogramRelationship(models.Model):
    subprogram = models.ForeignKey(Subprogram, on_delete=models.CASCADE, related_name="+")
    person = ParentalKey('Person', related_name='subprograms')
    group = models.CharField(choices=GROUPING_OPTIONS, max_length=50, blank=True, null=True, help_text='Set grouping for subprogram\'s our people page')
    fellowship_position = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Set subprogram-specific fellowhip information"
    )
    fellowship_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    panels = [
        FieldPanel('subprogram'),
        FieldPanel('group'),
        FieldPanel('fellowship_position'),
        FieldPanel('fellowship_year')
    ]

class PersonTopicRelationship(models.Model):
    topic = models.ForeignKey('issue.IssueOrTopic', on_delete=models.CASCADE, related_name="+")
    person = ParentalKey('person.Person', related_name="topics")

    panels = [
        PageChooserPanel('topic', 'issue.IssueOrTopic')
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
    sort_priority = models.CharField(
        choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')),
        blank=True, null=True, max_length=50,
        help_text='This will override alphabetical ordering.'
    )
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

    expertise = models.ManyToManyField(
        'issue.IssueOrTopic',
        through=PersonTopicRelationship,
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
    ], null=True, blank=True)

    role = models.CharField(choices=ROLE_OPTIONS, max_length=50)
    former = models.BooleanField(default=False, help_text="Select if person no longer serves above role.")
    fellowship_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
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
                FieldPanel('fellowship_year'),
                FieldPanel('expert'),
                FieldPanel('leadership'),
                FieldPanel('sort_priority'),
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
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle', 'report.Report', 'in_depth.InDepthProject']),
            PageChooserPanel(
                'feature_work_2',
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle', 'report.Report', 'in_depth.InDepthProject']),
            PageChooserPanel(
                'feature_work_3',
                ['article.Article', 'blog.BlogPost', 'book.Book', 'event.Event', 'issue.IssueOrTopic', 'podcast.Podcast', 'policy_paper.PolicyPaper', 'press_release.PressRelease', 'quoted.Quoted', 'weekly.WeeklyArticle', 'report.Report', 'in_depth.InDepthProject']),
        ], heading="Featured Work To Highlight on Bio Page", classname="collapsible"),
    ]

    parent_page_types = ['OurPeoplePage']
    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField('position_at_new_america', boost=0.33),
        index.SearchField('long_bio', boost=0.01),
        index.SearchField('short_bio', boost=0.33),
        index.SearchField('role', boost=0.01),

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
        verbose_name = 'Person'


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns everyone from the Person model
    """
    parent_page_types = ['home.HomePage']
    subpage_types = ['Person', 'BoardAndLeadershipPeoplePage']

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
        context['ourpeoplepage'] = OurPeoplePage.objects.filter(slug='our-people').first()

        return context

    class Meta:
        verbose_name = "Our People Page"


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

class ProgramPeoplePage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = []

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('story_image')
    ]

    class Meta:
        verbose_name = "Our People Page"


class BoardAndLeadershipPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program or Subprogram
    """
    parent_page_types = ['home.HomePage', 'OurPeoplePage']
    subpage_types = []

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

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

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('story_image')
    ]

    def get_context(self, request):
        context = super(BoardAndLeadershipPeoplePage, self).get_context(request)
        context['ourpeoplepage'] = OurPeoplePage.objects.filter(slug='our-people').first()

        return context

    class Meta:
        verbose_name = "Our Staff and Leadership Page"
