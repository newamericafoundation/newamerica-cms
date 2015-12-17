from django.db import models
from django.contrib.auth.models import User
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram



class PostProgramRelationship(models.Model):
    """
    Through model that maps the many to many relationship 
    between Post and Programs
    """
    
    program = models.ForeignKey(Program, related_name="+")
    post = ParentalKey('Post', related_name='programs')

    panels = [
        FieldPanel('program'),
    ]

class PostSubprogramRelationship(models.Model):
    """
    Through model that maps the many to many relationship 
    between Post and Subprograms
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

    parent_programs = models.ManyToManyField(Program, through=PostProgramRelationship, blank=True)

    post_subprogram = models.ManyToManyField(Subprogram, through=PostSubprogramRelationship, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
    ]

    is_creatable = False




class Book(Post):
    """
    Book class that inherits from the abstract Post model
    and creates pages for Books. 
    """
    pass


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