from __future__ import unicode_literals
import json

from django.db import models

from home.models import Post

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import PageChooserBlock

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results
from home.models import AbstractHomeContentPage

class Thread(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['ThreadArticle']

    featured_page_1 = models.ForeignKey(
        'home.Post',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    featured_page_2 = models.ForeignKey(
        'home.Post',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    featured_page_3 = models.ForeignKey(
        'home.Post',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('featured_page_1'),
        FieldPanel('featured_page_2'),
        FieldPanel('featured_page_3'),
    ] # x

    class Meta:
        verbose_name = "The Thread"


class ThreadEdition(Page):
    parent_page_types = []
    subpage_types = []


class ThreadArticle(Post):
    parent_page_types = ['Thread']
    subpage_types = []

    class Meta:
        verbose_name = 'Article in The Thread'


class AllThreadArticlesHomePage(AbstractHomeContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Thread Articles Homepage'

    @property
    def content_model(self):
        return ThreadArticle
