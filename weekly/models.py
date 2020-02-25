from __future__ import unicode_literals
import json

from home.models import Post

from wagtail.core.models import Page, PageRevision
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import PageChooserBlock

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results
from home.models import AbstractHomeContentPage

class Weekly(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['WeeklyArticle']

    class Meta:
        verbose_name = "Weekly Editions"


class WeeklyEdition(Page):
    parent_page_types = []
    subpage_types = []


class WeeklyArticle(Post):
    parent_page_types = ['Weekly']
    subpage_types = []

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

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
