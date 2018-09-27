from django.db import models

from home.models import Post

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class Quoted(Post):
    """
    Quoted class that inherits from the abstract
    Post model and creates pages for Quoted pages
    where New America was in the news.
    """
    parent_page_types = ['ProgramQuotedPage', 'programs.BlogProject', 'programs.BlogSeries']
    subpage_types = []

    source = models.TextField(max_length=8000, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True, max_length=500)

    content_panels = Post.content_panels + [
        FieldPanel('source'),
        FieldPanel('source_url'),
    ]

    class Meta:
        verbose_name = "In The News Piece"


class AllQuotedHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Quoted piece from the Quoted model
    for the organization-wide Quoted Homepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllQuotedHomePage,
            Quoted
        )

    @property
    def content_model(self):
        return Quoted

    class Meta:
        verbose_name = "In The News Homepage"


class ProgramQuotedPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Quoted pieces associated with a specific Program
    or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Quoted']

    def get_context(self, request):
        return get_program_and_subprogram_posts(
            self,
            request,
            ProgramQuotedPage,
            Quoted
        )

    @property
    def content_model(self):
        return Quoted

    class Meta:
        verbose_name = "In the News Homepage"
