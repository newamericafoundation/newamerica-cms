from home.models import Post

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage
from home.models import AbstractHomeContentPage

class PressRelease(Post):
    """
    Press Release class that inherits from the abstract
    Post model and creates pages for Press Releases.
    """
    parent_page_types = ['ProgramPressReleasesPage']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Post.content_panels + [
        FieldPanel('attachment'),
    ]

    class Meta:
        verbose_name = 'Press Release'


class AllPressReleasesHomePage(AbstractHomeContentPage):
    """
    A page which inherits from the abstract Page model and
    returns every Press Release in the PressRelease model
    for the organization-wide Press Release Homepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    @property
    def content_model(self):
        return PressRelease

    class Meta:
        verbose_name = "Homepage for all Press Releases"


class ProgramPressReleasesPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Press Releases associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['PressRelease']

    @property
    def content_model(self):
        return PressRelease

    class Meta:
        verbose_name = "Press Releases Homepage"
