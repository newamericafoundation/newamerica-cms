from django.db import models

from wagtail.wagtailcore.models import Page

from post.models import Post

class Book(Post):
    """
    Book class that inherits from the abstract Post
    model and creates pages for Books.
    """
    pass


class AllBooksHomePage(Page):
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(AllBooksHomePage, self).get_context(request)

        context['books'] = Book.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Books"


# class ProgramBooksPageHomePage(Page):
#     