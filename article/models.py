from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from mysite.helpers import paginate_results, get_posts_and_programs


class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    parent_page_types = ['ProgramArticlesPage']
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
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    def get_context(self, request):
        context = super(AllArticlesHomePage, self).get_context(request)

        all_posts = Article.objects.all().order_by("-date")

        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Articles and Op-Eds"


class ProgramArticlesPage(Page):
    """
    A page which inherits from the abstract Page model and
    returns all Articles associated with a specific Program
    or Subprogram
    """

    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Article']

    def get_context(self, request):
        return get_posts_and_programs(
            self,
            request,
            ProgramArticlesPage,
            Article
        )

    class Meta:
        verbose_name = "Articles and Op-Eds Homepage for Program and Subprograms"
