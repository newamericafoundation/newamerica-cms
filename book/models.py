from django.db import models

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from home.models import Post

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class Book(Post):
    """
    Book class that inherits from the abstract Post
    model and creates pages for Books.
    """
    publication_cover_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Post.content_panels + [
        ImageChooserPanel('publication_cover_image'),
    ]

    parent_page_types = ['ProgramBooksPage']
    subpage_types = []

    class Meta:
        verbose_name = 'Book'


class AllBooksHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Book in the Book model
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    @property
    def content_model(self):
        return Book

    class Meta:
        verbose_name = "Homepage for all Books"


class ProgramBooksPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Books associated with a specific program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Book']

    @property
    def content_model(self):
        return Book

    class Meta:
        verbose_name = "Books Homepage"
