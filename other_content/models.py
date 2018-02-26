from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage


class OtherPost(Post):
    """
    """
    parent_page_types = ['ProgramOtherPostsPage', 'OtherPostCategory']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False)),
    ], null=True)

    content_panels = Post.content_panels + [
        StreamFieldPanel('attachment'),
    ]

    other_content_type = models.ForeignKey(
        'other_content.ProgramOtherPostsPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    category = models.ForeignKey(
        'other_content.OtherPostCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def save(self, *args, **kwargs):
        parent = self.get_parent().specific
        if type(parent) == OtherPostCategory:
            self.category = parent
            self.other_content_type = parent.get_parent().specific
        else:
             self.other_content_type = parent

        super(OtherPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Other Post'

class AllOtherPostsHomePage(AbstractHomeContentPage):
    """
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    @property
    def content_model(self):
        return OtherPost

    class Meta:
        verbose_name = "Homepage for all Other Posts"

class ProgramOtherPostsPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    all Blog Posts associated with a specific Program or
    Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['OtherPost', 'OtherPostCategory']

    singular_title = models.CharField(max_length=255)
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
        FieldPanel('singular_title'),
        FieldPanel('subheading'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    @property
    def content_model(self):
        return OtherPost

    class Meta:
        verbose_name = "Homepage for Other Posts Program and Subprograms"

class OtherPostCategory(Page):
    """
    """
    parent_page_types = ['ProgramOtherPostsPage']
    subpage_types = ['OtherPost']

    class Meta:
        verbose_name = 'Category'
