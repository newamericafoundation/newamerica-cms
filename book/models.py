from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from home.models import Post

from mysite.helpers import paginate_results, get_posts_and_programs


class Book(Post):
    """
    Book class that inherits from the abstract Post
    model and creates pages for Books.
    """
    publication_cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Post.content_panels + [
        ImageChooserPanel('publication_cover_image'),
    ]

    parent_page_types = ['ProgramBooksPage', ]
    subpage_types = []


class AllBooksHomePage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every Book in the Book model
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = []

    def get_context(self, request):
        context = super(AllBooksHomePage, self).get_context(request)

        all_posts = Book.objects.all().order_by("-date")
        context['all_posts'] = paginate_results(request, all_posts)

        return context

    class Meta:
        verbose_name = "Homepage for all Books"


class ProgramBooksPage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns all Books associated with a specific program which 
    is determined using the url path
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Book']
    
    def get_context(self, request):
        return get_posts_and_programs(self, request, ProgramBooksPage, Book)

    class Meta:
        verbose_name = "Books Homepage for Program and Subprogram"
