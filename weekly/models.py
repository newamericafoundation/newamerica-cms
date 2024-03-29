from __future__ import unicode_literals
import json

from home.models import Post

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import PageChooserBlock

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results
from home.models import AbstractHomeContentPage

class Weekly(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['WeeklyArticle']

    class Meta:
        verbose_name = "The Weekly"


class WeeklyEdition(Page):
    parent_page_types = []
    subpage_types = []


class WeeklyArticle(Post):
    parent_page_types = ['Weekly']
    subpage_types = []

    class Meta:
        verbose_name = 'Weekly Article'


class AllWeeklyArticlesHomePage(AbstractHomeContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Weekly Articles Homepage'

    @property
    def content_model(self):
        return WeeklyArticle
