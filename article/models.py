from django.db import models

from home.models import Post

from programs.models import Program

from wagtail.wagtailcore.models import Page


class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    parent_page_types = ['ProgramArticlesPage',]
    subpage_types = []


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

        context['articles'] = Article.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Articles"


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

        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        context['articles'] = Article.objects.filter(parent_programs=program)
        context['program'] = program
        return context

    class Meta:
        verbose_name = "Articles Homepage for Program"
