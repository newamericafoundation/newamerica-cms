import json
from home.models import Post
import datetime

from django import forms
from django.db import models
from django.utils.text import slugify

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from programs.models import AbstractContentPage
from wagtailautocomplete.edit_handlers import AutocompletePanel

from multiselectfield import MultiSelectField
from .utils import MONTH_CHOICES, DATA_TYPE_CHOICES
class ProgramSurveysPage(AbstractContentPage):
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Survey', 'Commentary', 'SurveyValuesIndex']
    class Meta:
        verbose_name = "Surveys Homepage"

    def __str__(self):
        return self.title

class SurveyOrganization(Page):
    parent_page_types = ['SurveyValuesIndex']    
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Organizations'

class DemographicKey(Page):
    parent_page_types = ['SurveyValuesIndex']
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Demographic Keys'

class SurveyTags(Page):
    parent_page_types = ['SurveyValuesIndex']
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Tags'

class SurveyValuesIndex(Page):
    parent_page_types = ['ProgramSurveysPage']
    subpage_type = ['SurveyOrganization', 'DemographicKey', 'SurveyTags']
    class Meta:
        verbose_name = "Surveyindex Homepage"

    def __str__(self):
        return self.title


class Survey(Post):
    template = 'survey/survey.html'
 
    parent_page_types = ['ProgramSurveysPage']

    org = ParentalManyToManyField('SurveyOrganization', related_name='SurveyOrganization', blank=True)
    year = models.IntegerField(help_text='Year Survey was condicted.', blank=True, default=2000)
    month = models.IntegerField(choices=MONTH_CHOICES, default=None, help_text='Month Survey was condicted, if applicable.')
    sample_number = models.CharField(max_length=250, blank=True, null=True)
    sample_demos = models.CharField(max_length=250, blank=True, null=True, help_text='Text displayed on the dashboard')
    demos_key = ParentalManyToManyField('DemographicKey', help_text='Indexable demographic groups', blank=True, default=False)
    findings = RichTextField(blank=True, null=True, max_length=12500)
    data_type = MultiSelectField(choices=DATA_TYPE_CHOICES, default=['QUANT', 'QUAL'])
    national = models.BooleanField(default=True)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    assoc_commentary = ParentalManyToManyField('Commentary', blank=True, through='Commented_Survey', related_name='surveys')
    
    content_panels = [
      MultiFieldPanel([
        FieldPanel('date'),
      ], heading='Survey Created'),
      MultiFieldPanel([
        AutocompletePanel('org'),
        FieldPanel('year'),
        FieldPanel('month'),
        FieldPanel('sample_number'),
        FieldPanel('sample_demos'),
        AutocompletePanel('demos_key'),
        FieldPanel('data_type', widget=forms.CheckboxSelectMultiple),
        FieldPanel('national'),
        FieldPanel('findings'),
        AutocompletePanel('assoc_commentary')
      ], heading='Survey Data'),
      MultiFieldPanel([
        FieldPanel('link'),
        FieldPanel('file')
      ])
    ]


class Commentary(Post, RoutablePageMixin):
  template = 'survey/commentary.html'

  parent_page_types = ['ProgramSurveysPage']

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