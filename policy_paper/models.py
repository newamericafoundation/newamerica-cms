from django.db import models

from home.models import Post

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import URLBlock
from wagtail.documents.blocks import DocumentChooserBlock

from newamericadotorg.helpers import paginate_results, get_program_and_subprogram_posts, get_org_wide_posts
from programs.models import AbstractContentPage

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
    publication_cover_image_alt = models.TextField(
        default='',
        blank=True,
        verbose_name='Publication cover image alternative text',
        help_text='A concise description of the image for users of assistive technology.',
    )

    paper_url = StreamField([
        ('policy_paper_url', URLBlock(required=False, null=True)),
    ], null=True, blank=True, use_json_field=True)

    attachment = StreamField([
        ('attachment', DocumentChooserBlock(required=False, null=True)),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Post.content_panels + [
        FieldPanel('paper_url'),
        FieldPanel('attachment'),
        FieldPanel('publication_cover_image'),
        FieldPanel('publication_cover_image_alt'),
    ]

    def get_context(self, request):
        context = super(PolicyPaper, self).get_context(request);
        for block in self.body:
            if block.block_type == 'panels':
                context['panels'] = block.value;
        return context;

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

    @property
    def content_model(self):
        return PolicyPaper

    class Meta:
        verbose_name = "Homepage for all Policy Papers"


class ProgramPolicyPapersPage(AbstractContentPage):
    """
    A page which inherits from the abstract Page model and
    returns all Policy Papers associated with a specific
    Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['PolicyPaper']

    @property
    def content_model(self):
        return PolicyPaper

    class Meta:
        verbose_name = "Policy Papers Homepage"
