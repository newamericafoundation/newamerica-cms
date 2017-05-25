from django.conf import settings
from newamericadotorg.api.helpers import newamericadotorg_content_types
from programs.models import Program, Subprogram
from issue.models import IssueOrTopic

def debug(request):
    return {'DEBUG': settings.DEBUG}

def program_data(request):
    '''
    For sitewide context_processor
    Programs and related projects or topics
    '''
    program_data = []
    programs = Program.objects.in_menu().order_by("title").exclude(location=True)
    for p in programs:
        program_data.append({
            'program': p,
            'projects': p.get_children().type(Subprogram).live().in_menu(),
            'topics': p.get_children().type(IssueOrTopic).live().in_menu()
        })

    return { 'program_data': program_data }

def content_types(request):
    '''
    For sitewide context_processor
    All available content_types
    '''
    # content_classes = Post.__subclasses__()
    # content_types = []
    # for c in content_classes:
    #     content_types.append({
    #         'api_name': c._meta.model_name,
    #         'name': c._meta.verbose_name
    #     })

    return { 'content_types': newamericadotorg_content_types }
