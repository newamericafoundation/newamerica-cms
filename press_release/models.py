from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

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
    ], null=True, blank=True)

    content_panels = Post.content_panels + [
        StreamFieldPanel('attachment'),
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

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllPressReleasesHomePage,
            PressRelease
        )

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
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['PressRelease']

    def get_context(self, request):
        return get_program_and_subprogram_posts(
            self,
            request,
            ProgramPressReleasesPage,
            PressRelease
        )

    @property
    def content_model(self):
        return PressRelease

    class Meta:
        verbose_name = "Press Releases Homepage"
