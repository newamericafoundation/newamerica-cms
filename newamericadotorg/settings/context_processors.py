from django.conf import settings
from programs.models import Program, Subprogram, AbstractContentPage
from issue.models import IssueOrTopic
from wagtail.wagtailcore.models import Page
from home.models import HomePage, AbstractHomeContentPage

def debug(request):
    return {'DEBUG': settings.DEBUG}

def program_data(request):
    '''
    For sitewide context_processor
    Programs and related subprograms or topics
    '''
    program_data = []
    programs = Program.objects.in_menu().order_by("title").exclude(location=True)

    for p in programs:
        program_data.append({
            'program': p,
            'subprograms': p.get_children().type(Subprogram).live().in_menu()
        })

    return { 'program_data': program_data }

def locations(request):
    locations = Program.objects.in_menu().order_by("title").filter(location=True)

    return {
        'locations': locations
    }

def about_pages(request):
    pages = HomePage.objects.first().about_pages
    return {
        'about_pages': pages
    }

def content_types(request):
    '''
    For sitewide context_processor
    All available content_types
    '''
    typepages = Page.objects.live().type(AbstractHomeContentPage)
    types = []
    for p in typepages:
        p = p.specific
        types.append({
            'name': p.content_model._meta.verbose_name.title(),
            'api_name': p.content_model.__name__.lower(),
            'title': p.title,
            'slug': p.slug,
            'url': p.url
        })
    return { 'content_types':  types }
