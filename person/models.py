from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import URLBlock
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

from programs.models import Program

from search.search import content_search

# Through relationship that connects the Person model
# to the Program model so that a Person may belong
# to more than one Program
class PersonProgramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    person = ParentalKey('Person', related_name='programs')
    panels = [
        FieldPanel('program'),
    ]

class Person(Page):
    parent_page_types = ['OurPeoplePage',]
    subpage_types = []

    name = models.CharField(max_length=150)
    position_at_new_america = models.CharField(max_length=500, help_text="Position or Title at New America")
    email = models.EmailField()
    short_bio = models.TextField(max_length=1000, blank=True, null=True)
    long_bio = models.TextField(max_length=5000, blank=True, null=True)
    expert = models.BooleanField()
    location = models.CharField(max_length=200)
    photo = StreamField([
        ('photo', ImageChooserBlock(icon='image')),

    ])
    belongs_to_these_programs = models.ManyToManyField(Program, through=PersonProgramRelationship, blank=True)

    social_media = StreamField([
        ('twitter', URLBlock(required=False, help_text='Twitter Handle', icon='user')),
        ('facebook',URLBlock(required=False, help_text='Facebook Profile', icon='user')),
        ('youtube',URLBlock(required=False, help_text='YouTube Channel', icon='media')),
        ('google_plus',URLBlock(required=False, help_text='Google+ Profile', icon='user')),
        ('linkedin',URLBlock(required=False, help_text='LinkedIn Profile', icon='user')),
        ('tumblr',URLBlock(required=False, help_text='Tumblr', icon='user')),
    ])

    ROLE_OPTIONS = (
        ('Board Member', 'Board Member'),
        ('Staff', 'Staff'),
        ('New America Fellow', 'New America Fellow'),
        ('Program Fellow', 'Program Fellow'),
    )
    role = models.CharField(choices=ROLE_OPTIONS, max_length=50)

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('position_at_new_america'),
        FieldPanel('email'),
        FieldPanel('short_bio'),
        FieldPanel('long_bio', classname="full"),
        InlinePanel('programs', label=("Belongs to these Programs")),
        FieldPanel('role'),
        FieldPanel('expert'),
        StreamFieldPanel('photo'),
        StreamFieldPanel('social_media'),
    ]

    search_fields = (
        index.FilterField('program_id'),
        index.FilterField('live'),
    )


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns everyone from the Person model
    """

    parent_page_types = ['home.HomePage',]
    subpage_types = ['Person', ]

    def get_context(self, request):
        context = super(OurPeoplePage, self).get_context(request)
        search_query = request.GET.get('query', None)

        if search_query: 
            content_search(request, Person, context)
        else:
            context['people'] = Person.objects.all()

        return context

    class Meta:
        verbose_name = "Homepage for all People in NAF"


class ExpertPage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone who is marked as an expert from the Person model
    """
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(ExpertPage, self).get_context(request)

        context['non_program_experts'] = Person.objects\
            .filter(belongs_to_these_programs=None)\
            .filter(expert=True)\
            .order_by('-name')

        context['all_programs'] = Program.objects.all()

        return context


class ProgramPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and returns
    everyone from the Person model for a specific program which is
    determined using the url path
    """
    parent_page_types = ['programs.Program',]
    subpage_types = []

    def get_context(self, request):
        context = super(ProgramPeoplePage, self).get_context(request)

        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        context['people'] = Person.objects.filter(belongs_to_these_programs=program)
        context['program'] = program
        return context

    class Meta:
        verbose_name = "Our People Page for Programs"
