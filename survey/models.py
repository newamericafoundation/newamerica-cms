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
from taggit.models import TaggedItemBase
from wagtailautocomplete.edit_handlers import AutocompletePanel


class ProgramSurveysPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Articles associated with a specific Program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Survey', 'Commentary', 'SurveyValuesIndex']

    @property
    def content_model(self):
        return Survey

    class Meta:
        verbose_name = "Surveys Homepage"

    def __str__(self):
        return self.title

class SurveyOrganization(Page):
    parent_page_types = ['SurveyValuesIndex', 'ProgramSurveysPage']
    subpage_type = []
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
      test = ProgramSurveysPage.objects.first().title
    
      orgs_index_page = SurveyValuesIndex.objects.first()
      title = value

      new = cls(title=value)
      orgs_index_page.add_child(instance=new)
      orgs_index_page.save()
      return new

    def clean(self):
      """Override the values of title and slug before saving."""
      super().clean()
      if not self.slug:
        self.slug = slugify(self.title)   
  
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Survey Organizations'



class DemographicKey(Page):
    parent_page_types = ['SurveyValuesIndex', 'ProgramSurveysPage']
    subpage_type = []
    
    @classmethod
    def autocomplete_create(cls: type, value: str):
      test = ProgramSurveysPage.objects.first().title
    
      orgs_index_page = SurveyValuesIndex.objects.first()
      title = value

      new = cls(title=value)
      orgs_index_page.add_child(instance=new)
      orgs_index_page.save()
      return new

    def clean(self):
      """Override the values of title and slug before saving."""
      super().clean()
      # self.title = '%s %s' % (self.lable)
      if not self.slug:
        self.slug = slugify(self.title)   
  
    
    def __str__(self):
      return self.title
    class Meta:
        verbose_name_plural = 'Demographic Keys'

class SurveyValuesIndex(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Articles associated with a specific Program
    or Subprogram
    """

    parent_page_types = ['ProgramSurveysPage']
    subpage_type = ['SurveyOrganization', 'DemographicKey']

    def get_orgs(self):
      return SurveyOrganization.objects.live().descendant_of(self)
  
    def get_context(self, request, *args, **kwargs):
      context = super(SurveyValuesIndex, self).get_context(request)

      orgs = self.get_orgs() 

      context['orgs'] = orgs

      return context

    @property
    def content_model(self):
        return SurveyOrganization

    class Meta:
        verbose_name = "Surveyindex Homepage"

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
    # current_year = datetime.datetime.now().year
    # print(current_year)

    study_title= models.CharField(max_length=250, blank=True, null=True)
    org = ParentalManyToManyField('SurveyOrganization', related_name='SurveyOrganization', blank=True)
    year = models.IntegerField(help_text='Year Survey was condicted.', blank=True, default=2000)
    month = models.IntegerField(choices=MONTH_CHOICES, default=None, help_text='Month Survey was condicted, if applicable.')
    sample_number = models.CharField(max_length=250, blank=True, null=True)
    sample_demos = models.CharField(max_length=250, blank=True, null=True, help_text='Text displayed on the dashboard')
    demos_key = ParentalManyToManyField('DemographicKey', help_text='Indexable demographic groups', blank=True, default=False)
    findings = RichTextField(blank=True, null=True, max_length=12500)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    assoc_commentary = ParentalManyToManyField('Commentary', blank=True, through='Commented_Survey', related_name='surveys')
    content_panels = [
      MultiFieldPanel([
        FieldPanel('date'),
      ], heading='Survey Created'),
      MultiFieldPanel([
        FieldPanel('title'),
        AutocompletePanel('org'),
        FieldPanel('year'),
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