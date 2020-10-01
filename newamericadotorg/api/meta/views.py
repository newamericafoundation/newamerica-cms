from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.response import Response

from home.models import HomePage
from programs.models import Program

from newamericadotorg.settings.context_processors import content_types
from newamericadotorg.api.program.serializers import ProgramSerializer, SubscriptionSegmentSerializer

@method_decorator([cache_page(2*60)], name='get')
class MetaList(APIView):
    def get(self, request, format=None):
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

        return Response({
            'count': None,
            'next': None,
            'previous': None,
            'results': {
                'programs': programs,
                'content_types': types,
                'about_pages': abouts,
                'home_subscriptions': segments
            }
        })

class ContentList(APIView):
    def get(self, request, format=None):
        types = content_types(request)['content_types']
        return Response({
            'count': len(types),
            'next': None,
            'previous': None,
            'results': types
        })
