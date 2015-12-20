from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram
from person.models import Person


class PostAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Authors
    """
    author = models.ForeignKey(Person, related_name="+")
    post = ParentalKey('Post', related_name='authors')

    panels = [
        FieldPanel('author'),
    ]


class PostProgramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Programs
    """
    program = models.ForeignKey(Program, related_name="+")
    post = ParentalKey('Post', related_name='programs')

    panels = [
        FieldPanel('program'),
    ]


class PostSubprogramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Subprograms
    """
    subprogram = models.ForeignKey(Subprogram, related_name="+")
    post = ParentalKey('Post', related_name='subprograms')

    panels = [
        FieldPanel('subprogram'),
    ]


class Post(Page):
    """
    Abstract Post class that inherits from Page
    and provides a model template for other content
    type models
    """

    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('html', blocks.RawHTMLBlock()),
        ('image', ImageChooserBlock()),
    ])

    parent_programs = models.ManyToManyField(
        Program, through=PostProgramRelationship, blank=True)

    post_subprogram = models.ManyToManyField(
        Subprogram, through=PostSubprogramRelationship, blank=True)

    post_author = models.ManyToManyField(
        Person, through=PostAuthorRelationship, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
    ]

    is_creatable = False


class Book(Post):
    """
    Book class that inherits from the abstract Post
    model and creates pages for Books.
    """
    pass


class book_home_page(Page):
    def get_context(self, request):
        context = super(book_home_page, self).get_context(request)

        context['books'] = Book.objects.all()
        return context


class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    pass


class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    pass


class Podcasts(Post):
    """
    Podcast class that inherits from the abstract Post
    model and creates pages for Podcasts.
    """
    pass


class PolicyPaper(Post):
    """
    Policy paper class that inherits from the abstract
    Post model and creates pages for Policy papers.
    """
    pass


class About(Post):
    """
    About class that inherits from the abstract
    Post model and creates About Us pages.
    """
    pass


class Blog(Post):
    """
    Blog class that inherits from the abstract
    Post model and creates pages for blog posts.
    """
