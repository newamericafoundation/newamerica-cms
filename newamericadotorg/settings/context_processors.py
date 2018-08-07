from django.core.cache import cache
from django.conf import settings
import json
from wagtail.core.models import Page

from home.models import HomePage, AbstractHomeContentPage
from programs.models import Program, Subprogram, AbstractContentPage
from issue.models import IssueOrTopic

from newamericadotorg.api.program.serializers import ProgramSerializer, SubscriptionSegmentSerializer

def debug(request):
    return {'DEBUG': settings.DEBUG}

def program_data(request):
    '''
    For sitewide context_processor
    Programs and related subprograms or topics
    '''
    programdata = cache.get('NA_program_data', None)

    if programdata is None:
        programdata = []
        programs = Program.objects.in_menu().order_by("title").exclude(location=True)

        for p in programs:
            programdata.append({
                'program': p,
                'subprograms': p.get_children().type(Subprogram).live().in_menu()
            })
        cache.set('NA_program_data', programdata, 60 * 60)

    return { 'program_data': programdata }

def locations(request):
    locs = cache.get('NA_locations', None)
    if locs is None:
        locs = Program.objects.in_menu().order_by("title").filter(location=True)
        cache.set('NA_locations', locs, 60 * 60)

    return {
        'locations': locs
    }

def about_pages(request):
    aboutpages = cache.get('NA_about_pages', None)
    if aboutpages is None:
        aboutpages = HomePage.objects.first().about_pages
        cache.set('NA_about_pages', aboutpages, 60 * 60)

    return {
        'about_pages': aboutpages
    }

def content_types(request):
    '''
    For sitewide context_processor
    All available content_types
    '''
    contenttypes = cache.get('NA_content_types', None)
    if contenttypes is None:
        typepages = Page.objects.live().type(AbstractHomeContentPage)
        contenttypes = []
        for p in typepages:
            p = p.specific
            contenttypes.append({
                'name': p.content_model._meta.verbose_name.title(),
                'api_name': p.content_model.__name__.lower(),
                'title': p.title,
                'slug': p.slug,
                'url': p.url
            })
        cache.set('NA_content_types', contenttypes, 60 * 60);

    return { 'content_types':  contenttypes }

def meta(request):
    m = cache.get('NA_meta', None)

    if m is None:
        home = HomePage.objects.first()
        programs = ProgramSerializer(Program.objects.live().in_menu(), many=True).data
        types = content_types(request)['content_types']
        segments = []
        for s in home.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_title != '':
                seg['alternate_title'] = s.alternate_title
            segments.append(seg)

        if len(segments) == 0:
            segments = None

        about_pages = home.about_pages
        abouts = []
        for a in about_pages:
            abouts.append({ 'title': a.value.title, 'url': a.value.url })

        m = json.dumps({
            'programs': programs,
            'content_types': types,
            'about_pages': abouts,
            'home_subscriptions': segments
        })

        cache.set('NA_meta', m, 60 * 60 * 4)

    return { 'meta': m }

def ip_address(request):
    ip = None
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[1]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = None

    return { 'ip_address': ip }
