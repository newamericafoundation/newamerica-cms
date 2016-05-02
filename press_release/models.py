from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from mysite.helpers import paginate_results, get_posts_and_programs, get_org_wide_posts


class PressRelease(Post):
    """
    Press Release class that inherits from the abstract
    Post model and creates pages for Press Releases.
    """
    parent_page_types = ['ProgramPressReleasesPage']
    subpage_types = []

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ])

    content_panels = Post.content_panels + [
        StreamFieldPanel('attachment'),
    ]


class AllPressReleasesHomePage(Page):
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

    class Meta:
        verbose_name = "Homepage for all Press Releases"


class ProgramPressReleasesPage(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Press Releases associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['PressRelease']

    def get_context(self, request):
        return get_posts_and_programs(
            self,
            request,
            ProgramPressReleasesPage,
            PressRelease
        )

    class Meta:
        verbose_name = "Press Release Homepage for Program and Subprograms"
