from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from home.models import Post
from wagtail import blocks
from wagtail.fields import StreamField


from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class MediaLinks(blocks.StructBlock):
    label = blocks.TextBlock(max_length=30, required=False)
    description = blocks.TextBlock(max_length=65, required=False)
    url = blocks.URLBlock(required=True, default="https://www.")

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
    publication_cover_image_alt = models.TextField(
        default='',
        blank=True,
        verbose_name='Publication cover image alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

    media_links = StreamField(
        [
            ("featured", MediaLinks(required=False, null=True)),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=4,
        verbose_name='In the News',
    )

    content_panels = Post.content_panels + [
        FieldPanel('publication_cover_image'),
        FieldPanel('publication_cover_image_alt'),
        FieldPanel('media_links'),
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



