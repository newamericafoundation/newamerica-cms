from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail_headless_preview.models import PagePreview

from home.models import HomePage, ProgramAboutHomePage, ProgramAboutPage
from newamericadotorg.api.program.serializers import (
    AboutPageSerializer, ProgramDetailSerializer, ProgramSerializer,
    SubprogramSerializer, SubscriptionSegmentSerializer,
)
from newamericadotorg.api.report.serializers import ReportDetailSerializer
from newamericadotorg.settings.context_processors import content_types
from programs.models import Program, Subprogram


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


class PreviewView(APIView):
    def get(self, request):
        try:
            app_label, model = self.request.GET['content_type'].split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            token = self.request.GET['token']
        except Exception:
            return Response(
                {'detail': f'Unable to preview for content type {model}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page_preview = PagePreview.objects.get(content_type=content_type, token=token)
        if content_type.model == 'report':
            serializer = ReportDetailSerializer
        elif content_type.model == 'programabouthomepage':
            page_being_previewed = page_preview.as_page()
            program = page_being_previewed.program

            if isinstance(program, Subprogram):
                program_data = SubprogramSerializer(program).data
            elif isinstance(program, Program):
                program_data = ProgramDetailSerializer(program).data
            else:
                return Response(
                    {'detail': f'Unable to preview page with parent type {type(program)}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            about_page_data = AboutPageSerializer(page_being_previewed).data
            about_page_data['subpages'] = AboutPageSerializer(ProgramAboutPage.objects.descendant_of(page_being_previewed).live().in_menu(), many=True).data
            program_data['about'] = about_page_data

            # Extra data used used for establishing initial front-end route
            program_data['__extra'] = 'about'
            return Response(program_data)
        elif content_type.model == 'programaboutpage':
            page_being_previewed = page_preview.as_page()
            program = page_being_previewed.program

            if isinstance(program, Subprogram):
                program_data = SubprogramSerializer(program).data
            elif isinstance(program, Program):
                program_data = ProgramDetailSerializer(program).data
            else:
                return Response(
                    {'detail': f'Unable to preview page with parent type {type(program)}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            about_page = ProgramAboutHomePage.objects.child_of(program).live().first()
            about_page_data = AboutPageSerializer(about_page).data

            about_page_data['subpages'] = []

            for subpage in ProgramAboutPage.objects.descendant_of(about_page).live().in_menu():
                if subpage.pk == page_being_previewed.pk:
                    about_page_data['subpages'].append(AboutPageSerializer(page_being_previewed).data)
                else:
                    about_page_data['subpages'].append(AboutPageSerializer(subpage).data)

            program_data['about'] = about_page_data

            # Extra data used used for establishing initial front-end route
            program_data['__extra'] = f'about/{page_being_previewed.slug}'
            return Response(program_data)
        else:
            return Response(
                {'detail': f'Unable to preview content type {content_type.model}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return Response(serializer(page).data)
