from django.db import models

from home.models import Post

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.fields import RichTextField

from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage


class OtherPost(Post):
    """
    """
    parent_page_types = ['ProgramOtherPostsPage', 'OtherPostCategory']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False)),
    ], null=True, blank=True, use_json_field=True)

    archived_page = models.BooleanField(
        default=False,
        verbose_name="Archived Page"
    )

    last_updated = models.TextField(blank=True, null=True, help_text='Enter in the month and year this page was last updated (Example: April 2022).')

    content_panels = Post.content_panels + [
        FieldPanel('attachment'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("data_project_external_script"),
        FieldPanel("archived_page"),
        FieldPanel("last_updated"),
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
        verbose_name = "Other Posts Homepage"

class ProgramOtherPostsPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and returns
    all Blog Posts associated with a specific Program or
    Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
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
    story_image_alt = models.TextField(
        default='',
        blank=True,
        verbose_name='Story image alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

    content_panels = Page.content_panels + [
        FieldPanel('singular_title'),
        FieldPanel('subheading'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        FieldPanel('story_image'),
        FieldPanel('story_image_alt'),
    ]

    @property
    def content_model(self):
        return OtherPost

    class Meta:
        verbose_name = "Other Posts Homepage"

class OtherPostCategory(Page):
    """
    """
    parent_page_types = ['ProgramOtherPostsPage']
    subpage_types = ['OtherPost']

    class Meta:
        verbose_name = 'Category'

class FullPageEmbed(Page):
    parent_page_types = ['home.HomePage', 'programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = []

    embed_url = models.URLField()
    subheading = models.CharField(max_length=255, blank=True, null=True)
    include_header_footer = models.BooleanField(default=True, help_text="If true, the header and footer will be included in the page.")

    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
        FieldPanel('embed_url'),
        FieldPanel('include_header_footer'),
    ]

    # These pages are not indexed for search
    search_fields = []
    
    
