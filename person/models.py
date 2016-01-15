from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import URLBlock

from programs.models import Program


class Person(Page):
    name = models.CharField(max_length=150)
    position_at_new_america = models.CharField(max_length=500, help_text="Position or Title at New America")
    email = models.EmailField()
    short_bio = models.TextField(max_length=1000, blank=True, null=True)
    long_bio = models.TextField(max_length=5000, blank=True, null=True)
    belongs_to_program = models.ForeignKey(Program, blank=True, null=True, help_text="The Program this person works for")
    expert = models.BooleanField()
    location = models.CharField(max_length=200)
    photo = StreamField([
        ('photo', ImageChooserBlock(icon='image')),
    
    ])
    
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
        FieldPanel('belongs_to_program'),
        FieldPanel('role'),
        FieldPanel('expert'),
        StreamFieldPanel('photo'),
        StreamFieldPanel('social_media'),
    ]

    parent_page_types = ['OurPeoplePage',]
    subpage_types = []


class OurPeoplePage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns everyone from the Person model
    """

    parent_page_types = ['home.HomePage',]
    subpage_types = ['Person', ]

    def get_context(self, request):
        context = super(OurPeoplePage, self).get_context(request)

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

        context['experts'] = Person.objects.filter(expert=True)
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
        context['people'] = Person.objects.filter(program=program)
        context['program'] = program
        return context

    class Meta:
        verbose_name = "Our People Page for Programs"