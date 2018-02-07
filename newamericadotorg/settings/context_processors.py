from django.conf import settings
from newamericadotorg.api.helpers import newamericadotorg_content_types
from programs.models import Program, Subprogram
from issue.models import IssueOrTopic
from home.models import HomePage

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
    return { 'content_types': newamericadotorg_content_types }
