from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from programs.models import AbstractContentPage

class CustomContentType(Post):
    '''
    Custom content types are thought of for a very narrow use case: Legislative Filings and Congressional Hearings.
    We want to discourage reckless use of this type, so all custom content type posts must be organized by a category
    '''
    parent_page_types = ['CustomContentTypeCategory']

    class Meta:
        verbose_name = 'Custom'

class CustomContentTypeCategory(Page):

    parent_page_types = ['ProgramCustomContentTypePage']
    subpage_types = ['CustomContentType']

    class Meta:
        verbose_name = 'Category'

class ProgramCustomContentTypePage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    all Blog Posts associated with a specific Program or
    Subprogram
    """

    content_type_name = 'Custom Content Type'
    content_type_api_name = 'customcontenttype'

    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['CustomContentTypeCategory']

    subheading = RichTextField(blank=True, null=True)

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

    class Meta:
        verbose_name = "Custom Content Homepage"
