from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from modelcluster.models import ClusterableModel
from programs.models import Program

class Person(Page):
	name = models.CharField(max_length=150)
	bio = models.CharField(max_length=1000)
	program = models.ForeignKey(Program, blank=True, null=True)
	ROLE_OPTIONS = (
		('Board Member', 'Board Member'),
		('Staff', 'Staff'),
		('New America Fellow', 'New America Fellow'),
		('Program Fellow', 'Program Fellow'),
	)
	role = models.CharField(choices=ROLE_OPTIONS, max_length=50)

	content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('bio'),
        FieldPanel('program'),
        FieldPanel('role'),
    ]
