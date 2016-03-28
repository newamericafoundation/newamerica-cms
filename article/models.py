from django.db import models
from django.utils.text import slugify

from home.models import Post

from programs.models import Program, Subprogram

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from mysite.pagination import paginate_results


class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    parent_page_types = ['ProgramArticlesPage',]
    subpage_types = []

    source = models.TextField(max_length=8000, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    content_panels = Post.content_panels + [
        FieldPanel('source'),
        FieldPanel('source_url'),
    ]

    class Meta:
        verbose_name = "Article and Op-Ed"


class AllArticlesHomePage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every Article in the Article model for the Article
    homepage
    """
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(AllArticlesHomePage, self).get_context(request)

        all_posts = Article.objects.all()

        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Articles and Op-Eds"


class ProgramArticlesPage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns all Articles associated with a specific program
    which is determined using the url path
    """

    parent_page_types = ['programs.Program',]
    subpage_types = ['Article']
    
    def get_context(self, request):
        context = super(ProgramArticlesPage, self).get_context(request)

        program_title = self.get_ancestors()[2]

        program = Program.objects.get(title=program_title)
        
        all_posts = Article.objects.filter(parent_programs=program)
        
        context['all_posts'] = paginate_results(request, all_posts)

        context['program'] = program
        
        return context

    class Meta:
        verbose_name = "Articles and Op-Eds Homepage for Program"


class SubprogramArticlesPage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns all Articles associated with a specific subprogram
    which is determined using the depth 
    """

    parent_page_types = ['programs.Subprogram']
    subpage_types = ['Article']
    
    def get_context(self, request):
        context = super(SubprogramArticlesPage, self).get_context(request)

        subprogram_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        
        all_posts = Article.objects.filter(parent_programs=program)
        
        context['all_posts'] = paginate_results(request, all_posts)

        context['program'] = program
        
        return context

    class Meta:
        verbose_name = "Articles and Op-Eds Homepage for Program"

