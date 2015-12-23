from django.db import models

from wagtail.wagtailcore.models import Page

from home.models import Post
from programs.models import Program

class Book(Post):
    """
    Book class that inherits from the abstract Post
    model and creates pages for Books.
    """
    pass


class AllBooksHomePage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every Book in the Book model
    """
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(AllBooksHomePage, self).get_context(request)

        context['books'] = Book.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Books"


class ProgramBooksPage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns all Books associated with a specific program which 
    is determined using the url path
    """
    parent_page_types = ['programs.Program',]
    subpage_types = ['Book']
    
    def get_context(self, request):
        context = super(ProgramBooksPage, self).get_context(request)

        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        context['books'] = Book.objects.filter(parent_programs=program)
        return context

    class Meta:
        verbose_name = "Books Homepage for Program"
