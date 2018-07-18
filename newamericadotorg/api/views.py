import django_filters, math
from django.db.models import Q
from django.utils.timezone import localtime, now

from rest_framework import status, pagination, mixins, generics, views, response, filters
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django_filters.rest_framework import FilterSet

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from home.models import Post, HomePage, OrgSimplePage
from person.models import Person
from .serializers import (
    PostSerializer, AuthorSerializer, ProgramSerializer, ProgramDetailSerializer,
    SubprogramSerializer, HomeSerializer, TopicSerializer, TopicDetailSerializer, EventSerializer,
    WeeklyEditionSerializer, WeeklyArticleSerializer, WeeklyEditionListSerializer,
    SearchSerializer, ReportDetailSerializer,
    HomeDetailSerializer, SubscriptionSegmentSerializer
)
from .helpers import get_subpages
from newamericadotorg.settings.context_processors import content_types
from programs.models import Program, Subprogram, AbstractContentPage, AbstractProgram
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyArticle, WeeklyEdition
from report.models import Report
from other_content.models import OtherPost
from subscribe.campaign_monitor import update_subscriber
from ipware import get_client_ip

class PostFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    program_id = django_filters.CharFilter(name='parent_programs__id', lookup_expr='iexact')
    subprogram_id = django_filters.CharFilter(name='post_subprogram__id', lookup_expr='iexact')
    author_id = django_filters.CharFilter(name='post_author__id', lookup_expr='iexact')
    author_slug = django_filters.CharFilter(name='post_author__slug', lookup_expr="iexact")
    after = django_filters.DateFilter(name='date', lookup_expr='gte')
    before = django_filters.DateFilter(name='date', lookup_expr='lte')


    class Meta:
        model = Post
        fields = ['id', 'program_id', 'subprogram_id', 'before', 'after']

from newamericadotorg.api.expire_page_cache import expire_page_cache
class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = PostFilter

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type', None)
        other_content_type_title = self.request.query_params.get('other_content_type_title', None)
        ids = self.request.query_params.getlist('id[]', None)
        topic_id = self.request.query_params.get('topic_id', None)
        content_type_id = self.request.query_params.get('content_type_id', None)
        category = self.request.query_params.get('category', None)
        data_viz = self.request.query_params.get('data_viz', None)
        has_image = self.request.query_params.get('has_image', None)

        if other_content_type_title:
            posts = OtherPost.objects.live().public()\
                .filter(other_content_type__title=other_content_type_title)
            if category:
                posts = posts.filter(category__title=category)
        else:
            posts = Post.objects.live().not_type(Event).public()

        if has_image == 'true':
            queryset = queryset.filter(story_image__isnull=False)

        if content_type:
            if content_type == 'report':
                posts = posts.filter(content_type__model__in=['report', 'policypaper', 'indepthproject'])
            else:
                posts = posts.filter(content_type__model=content_type)


        posts = posts.order_by('-date').distinct()

        if topic_id:
            topics = IssueOrTopic.objects.get(pk=topic_id)\
                .get_descendants(inclusive=True).live()

            posts = posts.filter(post_topic__in=topics)

        if ids:
            posts = posts.filter(id__in=ids)

        if content_type_id:
            posts = posts.descendant_of(Page.objects.get(pk=content_type_id))

        if data_viz == 'true':
            posts = posts.exclude(data_project_external_script__isnull=True).exclude(data_project_external_script='')

        return posts;

class ReportDetail(generics.RetrieveAPIView):
    serializer_class = ReportDetailSerializer
    queryset = Report.objects.live()


from wagtail.wagtailsearch.backends import get_search_backend

class SearchList(generics.ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        results = Page.objects.live().search(search)
        query = Query.get(search)
        query.add_hit()
        from wagtail.wagtailcore.models import PageViewRestriction
        public_results =[]
        restrictions = PageViewRestriction.objects.all()
        for obj in results:
            private = False
            for restriction in restrictions:
                if obj.id == restriction.page.id or obj.is_descendant_of(restriction.page):
                    private = True

            if not private:
                public_results.append(obj)

        return public_results



class TopicFilter(django_filters.rest_framework.FilterSet):
    program_id = django_filters.CharFilter(name='parent_program__id', lookup_expr='iexact')

    class Meta:
        model = IssueOrTopic
        fields = ['program_id']

class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TopicFilter
    queryset = IssueOrTopic.objects.live().filter(depth=5)

class TopicDetail(generics.RetrieveAPIView):
    serializer_class = TopicDetailSerializer
    queryset = IssueOrTopic.objects.live()

BOOLEAN_CHOICES = (('false', 'False'), ('true', 'True'),)
from distutils.util import strtobool

class AuthorFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    slug = django_filters.CharFilter(name='slug', lookup_expr="iexact")
    program_id = django_filters.CharFilter(name='belongs_to_these_programs__id', lookup_expr='iexact')
    program_slug = django_filters.CharFilter(name='belongs_to_these_programs__slug', lookup_expr='iexact')
    subprogram_id = django_filters.CharFilter(name='belongs_to_these_subprograms__id', lookup_expr='iexact')
    role = django_filters.CharFilter(name='role', lookup_expr='iexact')
    leadership = django_filters.TypedChoiceFilter(choices=BOOLEAN_CHOICES,coerce=strtobool)
    name = django_filters.CharFilter(name='title', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = ['id','program_id', 'subprogram_id', 'name', 'role', 'leadership']

def get_edition_number(edition):
    if 'edition-' in edition.slug:
        return -int(edition.slug.split('-')[1])
    return -int(edition.slug)

class WeeklyPagination(pagination.LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000


class WeeklyList(generics.ListAPIView):
    serializer_class = WeeklyEditionListSerializer

    def get_queryset(self):
        queryset = WeeklyEdition.objects.live().public()
        return sorted(queryset, key=lambda edition: get_edition_number(edition));

class WeeklyDetail(generics.RetrieveAPIView):
    queryset = WeeklyEdition.objects.all()
    serializer_class = WeeklyEditionSerializer


class AuthorList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = AuthorFilter

    def get_queryset(self):
        queryset = Person.objects.live().order_by('sort_priority', 'last_name')\
            .exclude(role__icontains='External Author').distinct()
        topic_id = self.request.query_params.get('topic_id', None)
        former = self.request.query_params.get('former', None)
        has_image = self.request.query_params.get('has_image', None)
        include_fellows = self.request.query_params.get('include_fellows', None)

        if not include_fellows or include_fellows == 'false':
            queryset = queryset.exclude(role__icontains='fellow')

        if former == 'false':
            queryset = queryset.filter(former=False)
        elif former == 'true':
            queryset = queryset.filter(former=True)
        else:
            queryset = queryset.exclude(former=True)
        if has_image == 'true':
            queryset = queryset.filter(profile_image__isnull=False)

        if topic_id:
            topics = IssueOrTopic.objects.get(pk=topic_id)\
                .get_descendants(inclusive=True).live()

            queryset = queryset.filter(expertise__in=topics)

        return queryset

class FellowList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = AuthorFilter

    def get_queryset(self):
        queryset = Person.objects.live().order_by('fellowship_year', 'sort_priority', 'last_name').filter(role='Fellow')
        fellowship_year = self.request.query_params.get('fellowship_year', None)
        topic_id = self.request.query_params.get('topic_id', None)
        former = self.request.query_params.get('former', None)
        if former == 'false':
            queryset = queryset.filter(former=False)
        elif former == 'true':
            queryset = queryset.filter(former=True)

        if fellowship_year:
            try:
                queryset = queryset.filter(fellowship_year=int(fellowship_year))
            except ValueError:
                pass

        if topic_id:
            topics = IssueOrTopic.objects.get(pk=topic_id)\
                .get_descendants(inclusive=True).live()

            queryset = queryset.filter(expertise__in=topics)

        return queryset

class EventFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    program_id = django_filters.CharFilter(name='parent_programs__id', lookup_expr='iexact')
    subprogram_id = django_filters.CharFilter(name='post_subprogram__id', lookup_expr='iexact')
    program_slug = django_filters.CharFilter(name='parent_programs__slug', lookup_expr='iexact')
    subprogram_slug = django_filters.CharFilter(name='post_subprogram__slug', lookup_expr='iexact')
    topic_id = django_filters.CharFilter(name='topic__id', lookup_expr='iexact')
    after = django_filters.DateFilter(name='date', lookup_expr='gte')
    before = django_filters.DateFilter(name='date', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['id', 'program_id', 'subprogram_id', 'before', 'after', 'topic_id']

class EventList(generics.ListAPIView):
    serializer_class = EventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = EventFilter

    def get_queryset(self):
        ids = self.request.query_params.getlist('id[]', None)
        time_period = self.request.query_params.get('time_period', None)
        events = Event.objects.live().public().distinct()
        has_image = self.request.query_params.get('has_image', None)

        if time_period:
            today = localtime(now()).date()
            if time_period=='future':
                return events.filter(Q(date__gte=today)).order_by('date', 'start_time')
            elif time_period=='past':
                return events.filter(date__lt=today).order_by('-date', '-start_time')

        if has_image == 'true':
            events = events.filter(story_image__isnull=False)

        if not ids:
            return events.order_by('-date', '-start_time')

        return events.filter(id__in=ids).order_by('-date', '-start_time')

class MetaList(views.APIView):
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

        return response.Response({
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

class ContentList(views.APIView):
    def get(self, request, format=None):
        types = content_types(request)['content_types']
        return response.Response({
            'count': len(types),
            'next': None,
            'previous': None,
            'results': types
        })

import os
import requests
import json
class JobsList(views.APIView):
    def get(self, request, format=None):
        JAZZ_API_KEY = os.getenv('JAZZ_API_KEY')
        url = "https://api.resumatorapi.com/v1/jobs/status/open?apikey=%s" % JAZZ_API_KEY
        jobs = requests.get(url).json()
        return response.Response({
            'count': 0,
            'next': None,
            'previous': None,
            'results': jobs
        })

class ProgramFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    slug = django_filters.CharFilter(name='slug', lookup_expr='iexact')

    class Meta:
        model = Program
        fields = ['id', 'slug']

class ProgramDetail(generics.RetrieveAPIView):
    queryset = Program.objects.live()
    serializer_class = ProgramDetailSerializer

class ProgramList(generics.ListAPIView):
    serializer_class = ProgramSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = ProgramFilter

    def get_queryset(self):
        return Program.objects.in_menu().live().public().order_by('title').exclude(location=True)


class FellowshipList(views.APIView):
    def get(self, request, format=None):
        fellow_programs = Program.objects.in_menu().live().filter(fellowship=True)
        fellow_subprograms = Subprogram.objects.in_menu().live().filter(fellowship=True)
        fellow_programs = ProgramSerializer(fellow_programs, many=True).data
        fellow_subprograms = ProgramSerializer(fellow_subprograms, many=True).data
        fellowships = fellow_programs + fellow_subprograms
        return response.Response({
            'count': len(fellowships),
            'next': None,
            'previous': None,
            'results': fellowships
        })

class SubprogramFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    program_id = django_filters.CharFilter(name='parent_programs__id', lookup_expr='iexact')

    class Meta:
        model = Subprogram
        fields = ['id', 'program_id']

class SubprogramList(generics.ListAPIView):
    queryset = Subprogram.objects.live().order_by('title')
    serializer_class = SubprogramSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = SubprogramFilter

class SubprogramDetail(generics.RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SubprogramSerializer

class HomeDetail(generics.RetrieveAPIView):
    queryset = OrgSimplePage.objects.live()
    serializer_class = HomeDetailSerializer

@api_view(['POST'])
def subscribe(request):
    params = request.query_params
    recaptcha_response = params.get('g-recaptcha-response', None)
    if not recaptcha_response:
        return response.Response({
            'status': 'UNVERIFIED'
        });

    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify?response=%s&secret=%s' % (recaptcha_response, RECAPTCHA_SECRET_KEY)
    verification = urllib2.urlopen(recaptcha_url).read()
    verification = json.loads(verification)

    if not verification['success']:
        return response.Response({
            'status': 'UNVERIFIED'
        });

    subscriptions = params.getlist('subscriptions[]', None)
    job_title = params.get('job_title', None)
    org = params.get('organization', None)
    zipcode = params.get('zipcode', None)
    custom_fields = []

    if job_title:
        custom_fields.append({ 'key': 'JobTitle', 'value': job_title })
    if org:
        custom_fields.append({ 'key': 'Organization', 'value': org })
    if zipcode:
        custom_fields.append({ 'key': 'MailingZip/PostalCode', 'value': zipcode })
    if subscriptions:
        for s in subscriptions:
            custom_fields.append({ 'key': 'Subscriptions', 'value': s })

    status = update_subscriber(params.get('email'), params.get('name'), custom_fields)

    return response.Response({
        'status': status
    });
