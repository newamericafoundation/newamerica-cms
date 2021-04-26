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

class Thread(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['ThreadArticle']

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
