from django.db import models

from home.models import Post

from programs.models import Program

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel

from mysite.pagination import paginate_results


class Quoted(Post):
    """
    Quoted class that inherits from the abstract
    Post model and creates pages for Quoted pages
    where New America was in the news.
    """
    parent_page_types = ['ProgramQuotedPage']
    subpage_types = []

    source = models.TextField(max_length=8000, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    content_panels = Post.content_panels + [
        FieldPanel('source'),
        FieldPanel('source_url'),
    ]

    def get_page_type(self):
        type_name = 'quoted'
        return type_name

    class Meta:
        verbose_name = "In The News Piece"

class AllQuotedHomePage(Page):
    """
    A page which inherits from the abstract Page model and
    returns every Quoted piece from the Quoted model
    for the organization-wide Quoted Homepage 
    """
    parent_page_types = ['home.Homepage']
    subpage_types = []

    def get_context(self, request):
        context = super(AllQuotedHomePage, self).get_context(request)
        all_posts = Quoted.objects.all()

        context['all_posts'] = paginate_results(request, all_posts)

        return context
    class Meta:
        verbose_name = "Homepage for all In The News Pieces"


class ProgramQuotedPage(Page):
    parent_page_types = ['programs.Program']
    subpage_types = ['Quoted']

    def get_context(self, request):
        context = super(ProgramQuotedPage, self).get_context(request)
        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        
        all_posts = Quoted.objects.filter(parent_programs=program)
        context['all_posts'] = paginate_results(request, all_posts)

        context['program'] = program

        return context
    class Meta:
        verbose_name = "In the News Homepage for Programs"
