from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore.blocks import URLBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts


class PolicyPaper(Post):
    """
    Policy paper class that inherits from the abstract
    Post model and creates pages for Policy Papers.
    """
    parent_page_types = ['ProgramPolicyPapersPage']
    subpage_types = []

    publication_cover_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    paper_url = StreamField([
        ('policy_paper_url', URLBlock(required=False, null=True)),
    ])

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ])

    content_panels = Post.content_panels + [
        StreamFieldPanel('paper_url'),
        StreamFieldPanel('attachment'),
        ImageChooserPanel('publication_cover_image'),
    ]

    class Meta:
        verbose_name = 'Policy Paper'

class AllPolicyPapersHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every Policy Paper in the Policy Paper model
    for the organization wide Policy Paper Homepage
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    def get_context(self, request):
        return get_org_wide_posts(
            self,
            request,
            AllPolicyPapersHomePage,
            PolicyPaper
        )

    class Meta:
        verbose_name = "Homepage for all Policy Papers"


class ProgramPolicyPapersPage(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Policy Papers associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['PolicyPaper']

    def get_context(self, request):
        return get_program_and_subprogram_posts(
            self,
            request,
            ProgramPolicyPapersPage,
            PolicyPaper
        )

    class Meta:
        verbose_name = "Policy Paper Homepage for Programs and Subprograms"
