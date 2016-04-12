from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailcore.blocks import URLBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import PageChooserPanel, MultiFieldPanel

from modelcluster.fields import ParentalKey

from programs.models import Program, Subprogram

from mysite.helpers import paginate_results


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
    location = models.CharField(max_length=200)
    profile_image = models.ForeignKey(
        'wagtailimages.Image',
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
        null=True
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
        ('Board Member', 'Board Member'),
        ('Fellow', 'Fellow'),
        ('Central Staff', 'Central Staff'),
        ('Program Staff', 'Program Staff'),
        ('External Author/Former Staff', 'External Author/Former Staff'),
    )
    role = models.CharField(choices=ROLE_OPTIONS, max_length=50)

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
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('position_at_new_america'),
        FieldPanel('email'),
        FieldPanel('short_bio'),
        FieldPanel('long_bio', classname="full"),
        InlinePanel('programs',
            label=("Belongs to these Programs")),
        InlinePanel('subprograms',
            label=("Belongs to these Subprograms/Initiatives")),
        FieldPanel('role'),
        FieldPanel('expert'),
        FieldPanel('leadership'),
        ImageChooserPanel('profile_image'),
        MultiFieldPanel(
            [
                PageChooserPanel('feature_work_1'),
                PageChooserPanel('feature_work_2'),
                PageChooserPanel('feature_work_3'),
            ],
            heading="Featured Work To Highlight on Bio Page",
            classname="collapsible"
        ),
        StreamFieldPanel('social_media'),
    ]

    parent_page_types = ['OurPeoplePage']
    subpage_types = []

    def get_context(self, request):
        context = super(Person, self).get_context(request)
        featured_work = [
            self.feature_work_1, 
            self.feature_work_2, 
            self.feature_work_3
        ]

        context['featured_work'] = featured_work
        
        return context


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns everyone from the Person model
    """
    parent_page_types = ['home.HomePage']
    subpage_types = ['Person']

    page_description = RichTextField(blank=True, null=True)
    
    story_image = models.ForeignKey(
        'wagtailimages.Image',
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

        context['people'] = Person.objects.all().exclude(
            role='External Author/Former Staff')

        context['all_programs'] = Program.objects.all()

        context['all_our_people_pages'] = ProgramPeoplePage.objects.all()

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
        'wagtailimages.Image',
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
            .filter(belongs_to_these_programs=None)\
            .filter(expert=True)\
            .order_by('-title')

        context['all_programs'] = Program.objects.all()

        context['all_our_people_pages'] = ProgramPeoplePage.objects.all()

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
            all_posts = Person.objects.filter(
                belongs_to_these_programs=program
            )
        else:
            subprogram_title = self.get_ancestors()[3]
            program = Subprogram.objects.get(title=subprogram_title)
            all_posts = Person.objects.filter(
                belongs_to_these_subprograms=program
            )

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

    content_panels = Page.content_panels + [
        FieldPanel('page_description'),
        FieldPanel('role_query'),
    ]

    def get_context(self, request):
        context = super(BoardAndLeadershipPeoplePage, self).get_context(request)

        which_role = self.role_query

        if which_role == 'Leadership Team':
            all_people = Person.objects.filter(leadership=True)
        else:
            all_people = Person.objects.filter(role=which_role)

        context['people'] = paginate_results(request, all_people)

        return context

    class Meta:
        verbose_name = "Our People Page for Board of Directors, Central Staff, and Leadership Team"
