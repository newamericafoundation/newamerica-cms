import json
from home.models import Post
from person.models import Person
from programs.models import AbstractContentPage, Project

from django import forms
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from multiselectfield import MultiSelectField
from wagtailautocomplete.edit_handlers import AutocompletePanel

from .utils import MONTH_CHOICES, DATA_TYPE_CHOICES

class PageAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Survey Home Page and Authors
    """
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="+")
    page = ParentalKey('SurveysHomePage', related_name='authors')

    panels = [
        PageChooserPanel('author'),
    ]
    class Meta:
        ordering = ['pk']


class SurveysHomePage(AbstractContentPage):
    parent_page_types = ['programs.Project']
    subpage_types = ['Survey', 'Commentary', 'SurveyValuesIndex']

    partner_logo = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    about = RichTextField(
      max_length=1500,
      blank=True,
      verbose_name='About This Project'
    )
    page_author = models.ManyToManyField(
      Person,
      through=PageAuthorRelationship,
      blank=True
    )
    subheading = models.CharField(max_length=200, blank=True)
    methodology = RichTextField(max_length = 1500, blank=True)

    content_panels = [
      FieldPanel('title'),
      FieldPanel('subheading'),
      MultiFieldPanel([
        FieldPanel('about'),
        FieldPanel('methodology'),
        InlinePanel('authors', label="Authors"),
        ImageChooserPanel('partner_logo'),
      ], heading='About Page')
    ]

    search_fields = Page.search_fields + [
      index.RelatedFields('page_author', [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('position_at_new_america'),
      ]),
      ]

    def get_context(self, request):
        context = super(SurveysHomePage, self).get_context(request)
        context['authors'] = self.authors.order_by('pk')

        return context

    def save(self, *args, **kwargs):
      super(SurveysHomePage, self).save(*args, **kwargs)
      if self.get_children_count() == 0:
        self.add_child(instance=SurveyValuesIndex(title=self.title + " Values Index", slug=slugify(self.title + " Values Index")))

    @property	
    def content_model(self):	
      return SurveysHomePage
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
    parent_page_types = ['SurveysHomePage']
    subpage_type = ['SurveyOrganization', 'DemographicKey', 'SurveyTags']
    class Meta:
        verbose_name = "Surveyindex Homepage"

    def __str__(self):
        return self.title


class Survey(Post):
    template = 'survey/survey.html' 
    parent_page_types = ['SurveysHomePage']

    description = models.CharField(blank=True, null=True, max_length=500, help_text='A brief description of the survey. 500 chars max')
    org = ParentalManyToManyField('SurveyOrganization', related_name='SurveyOrganization', blank=True, verbose_name='Organization')
    year = models.IntegerField(help_text='Year Survey was conducted.', blank=True, default=2000)
    month = models.IntegerField(choices=MONTH_CHOICES, default=None, help_text='Month Survey was conducted, if applicable.')
    sample_number = models.IntegerField(blank=True, null=True)
    demos_key = ParentalManyToManyField('DemographicKey', help_text='Indexable demographic groups', blank=True, default=False, verbose_name='Demographics Keys')
    findings = RichTextField(blank=True, null=True, max_length=12500)
    data_type = MultiSelectField(choices=DATA_TYPE_CHOICES)
    national = models.BooleanField(default=True, verbose_name='Nationally Representative?', help_text='Indicates whether the survey was nationally representative or not.')
    link = models.URLField(blank=True, null=True, verbose_name='Link to Survey', help_text='Add a link to a webpage containing the survey details.')
    file = models.FileField(blank=True, null=True, verbose_name='Survey File', help_text='Add a file containing the survey details.')
    assoc_commentary = ParentalManyToManyField('Commentary', blank=True, through='Commented_Survey', related_name='surveys', verbose_name='Associated Commentary')
    tags =  ParentalManyToManyField('SurveyTags', help_text='Select from available tags', blank=True, default=False, verbose_name='Topics')
    content_panels = [
      MultiFieldPanel([
        FieldPanel('title'),
        FieldPanel('date'),
      ], heading='Survey Created'),
      MultiFieldPanel([
        FieldPanel('description'),
        AutocompletePanel('org'),
        FieldPanel('year'),
        FieldPanel('month'),
        FieldPanel('sample_number'),
        AutocompletePanel('demos_key'),
        AutocompletePanel('tags'),
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
    class Meta:
      verbose_name = 'Survey Reports'

    def __str__(self):
        return self.title

class Commentary(Post):
  template = 'survey/commentary.html'

  parent_page_types = ['SurveysHomePage']

  assoc_surveys = ParentalManyToManyField('Survey', through='Commented_Survey', blank=True, related_name='commentaries')

  content_panels = [
      FieldPanel('title'),
      FieldPanel('subheading'),
      FieldPanel('date'),
      StreamFieldPanel('body'),
      InlinePanel('authors', label=("Authors")),
      AutocompletePanel('assoc_surveys')
  ]

  class Meta:
      verbose_name = 'Insights & Analysis'

  def __str__(self):
        return self.title

class Commented_Survey(models.Model):
  survey=models.ForeignKey('Survey', on_delete=models.CASCADE, blank=True, null=True)
  commentary = models.ForeignKey('Commentary', on_delete=models.CASCADE, blank=True, null=True)
