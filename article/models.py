from django.db import models

from home.models import Post

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from newamericadotorg.helpers import get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    parent_page_types = ['ProgramArticlesPage']
    subpage_types = []

    source = models.TextField(max_length=8000, blank=True, null=True)
    source_url = models.URLField(max_length=1000, blank=True, null=True)

    content_panels = Post.content_panels + [
        FieldPanel('source'),
        FieldPanel('source_url'),
    ]

    class Meta:
        verbose_name = "Article/Op-Ed"


class AllArticlesHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Article in the Article model for the Article
    homepage
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    @property
    def content_model(self):
        return Article

    class Meta:
        verbose_name = "Articles/Op-Eds Homepage"


class ProgramArticlesPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Articles associated with a specific Program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Article']

    @property
    def content_model(self):
        return Article

    class Meta:
        verbose_name = "Articles/Op-Eds Homepage"
