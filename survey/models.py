import json
from home.models import Post

from django import forms
from django.db import models
from django.utils import timezone

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from programs.models import AbstractContentPage
from taggit.models import TaggedItemBase
from wagtailautocomplete.edit_handlers import AutocompletePanel


class ProgramSurveysPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Articles associated with a specific Program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Survey', 'Commentary']

    @property
    def content_model(self):
        return Survey

    class Meta:
        verbose_name = "Surveys Homepage"

    def __str__(self):
        return self.title

class Survey(Post, RoutablePageMixin):
    template = 'survey/survey.html'
    
    MONTH_CHOICES = (
      (0, 'N/A'),
      (1, 'January'),
      (2, 'February'),
      (3, 'March'),
      (4, 'April'),
      (5, 'May'),
      (6, 'June'),
      (7, 'July'),
      (8, 'August'),
      (9, 'September'),
      (10, 'October'),
      (11, 'November'),
      (12, 'December')
    )
    parent_page_types = ['ProgramSurveysPage']
    subpage_type=[]

    study_title= models.CharField(max_length=250, blank=True, null=True)
    org = ParentalManyToManyField('survey.Survey_Orgs')
    year = ParentalManyToManyField('survey.Survey_Years', help_text='Year Survey was condicted.')
    month = models.IntegerField(choices=MONTH_CHOICES, default=None, help_text='Month Survey was condicted, if applicable.')
    # Is this needed. Sample siez is non-standard and not displayed in the dashboard
    # sample_size = models.CharField(max_length=250)
    sample_number = models.CharField(max_length=250, blank=True, null=True)
    sample_demos = models.CharField(max_length=250, blank=True, null=True, help_text='Text displayed on the dashboard')
    demos_key = ParentalManyToManyField('survey.Demo_Key', help_text='Indexable demographic groups')
    findings = RichTextField(blank=True, null=True, max_length=12500)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    assoc_commentary = ParentalManyToManyField('Commentary', blank=True, through='Commented_Survey', related_name='surveys')
    content_panels = [
      MultiFieldPanel([
        FieldPanel('title'),
        FieldPanel('date'),
      ], heading='Survey Page Data'),
      MultiFieldPanel([
        FieldPanel('study_title'),
        AutocompletePanel('org'),
        AutocompletePanel('year'),
        FieldPanel('month'),
        FieldPanel('sample_number'),
        FieldPanel('sample_demos'),
        AutocompletePanel('demos_key'),
        FieldPanel('findings'),
        AutocompletePanel('assoc_commentary')
      ], heading='Survey Data'),
      MultiFieldPanel([
        FieldPanel('link'),
        FieldPanel('file')
      ])
    ]


# @todo find a way to dry this up.
@register_snippet
class Demo_Key(models.Model):
    title = models.CharField(blank=False, max_length=50)
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
        return cls.objects.create(title=value)
    
    def __str__(self):
      return self.title
    class Meta:
      verbose_name_plural = 'Demographics Keys'
        
@register_snippet
class Survey_Orgs(models.Model):
    title = models.CharField(blank=False, max_length=50)
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
        return cls.objects.create(title=value)
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Organizations'

@register_snippet
class Survey_Years(models.Model):
    title = models.CharField(blank=False, max_length=50)
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
        return cls.objects.create(title=value)
  
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Years'



class Commentary(Post, RoutablePageMixin):
  template = 'survey/commentary.html'

  parent_page_types = ['ProgramSurveysPage']
  subpage_types = []

  assoc_surveys = ParentalManyToManyField('Survey', through='Commented_Survey', blank=True, related_name='commentaries')

  content_panels = [
      FieldPanel('title'),
      FieldPanel('subheading'),
      FieldPanel('date'),
      StreamFieldPanel('body'),
      InlinePanel('authors', label=("Authors")),
      InlinePanel('topics', label=("Topics")),
      AutocompletePanel('assoc_surveys')
  ]

  class Meta:
      verbose_name = 'Expert Commentary'

  def __str__(self):
        return self.title

class Commented_Survey(models.Model):
  survey=models.ForeignKey('Survey', on_delete=models.CASCADE, blank=True, null=True)
  commentary=models.ForeignKey('Commentary', on_delete=models.CASCADE, blank=True, null=True)