from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts


class BlogPost(Post):
    """
    Blog class that inherits from the abstract
    Post model and creates pages for blog posts.
    """
    parent_page_types = ['ProgramBlogPostsPage']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False)),
    ], null=True)

    content_panels = Post.content_panels + [
        StreamFieldPanel('attachment'),
    ]

    class Meta:
        verbose_name = 'Blog Post'


class AllBlogPostsHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every Blog post in the BlogPost model for the
    Blog posts homepage
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllBlogPostsHomePage,
            BlogPost
        )

    class Meta:
        verbose_name = "Homepage for all Blog Posts"


class ProgramBlogPostsPage(Page):
    """
    A page which inherits from the abstract Page model and returns
    all Blog Posts associated with a specific Program or
    Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram']
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
        ImageChooserPanel('story_image'),
    ]

    def get_context(self, request):
        return get_program_and_subprogram_posts(
            self,
            request,
            ProgramBlogPostsPage,
            BlogPost)

    class Meta:
        verbose_name = "Blog Homepage for Program and Subprograms"
