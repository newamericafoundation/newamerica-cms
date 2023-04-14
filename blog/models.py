from django.db import models

from home.models import Post

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class BlogPost(Post):
    """
    Blog class that inherits from the abstract
    Post model and creates pages for blog posts.
    """
    parent_page_types = ['ProgramBlogPostsPage']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False)),
    ], null=True, blank=True)

    content_panels = Post.content_panels + [
        FieldPanel('attachment'),
    ]

    class Meta:
        verbose_name = 'Blog Post'


class AllBlogPostsHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Blog post in the BlogPost model for the
    Blog posts homepage
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    @property
    def content_model(self):
        return BlogPost

    class Meta:
        verbose_name = "New America Blog"


class ProgramBlogPostsPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    all Blog Posts associated with a specific Program or
    Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['BlogPost']

    subheading = RichTextField(blank=True, null=True)

    # Story excerpt and story image fields are to provide information
    # about the blog if it is featured on a homepage
    # or program landing page
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        FieldPanel('story_image'),
    ]

    @property
    def content_model(self):
        return BlogPost

    class Meta:
        verbose_name = "Blog Posts Homepage"
