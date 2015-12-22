from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page


class Article(Post):
    """
    Article class that inherits from the abstract Post
    model and creates pages for Articles.
    """
    pass


class ArticleHomePage(Page):
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(ArticleHomePage, self).get_context(request)

        context['articles'] = Article.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Articles"


