import django_filters, math
from django.db.models import Q
from django.utils.timezone import localtime, now

from rest_framework import status, pagination, mixins, generics, views, response, filters
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django_filters.rest_framework import FilterSet

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from home.models import Post, HomePage
from person.models import Person
from serializers import (
    PostSerializer, AuthorSerializer, ProgramSerializer, ProgramDetailSerializer,
    SubprogramSerializer, HomeSerializer, TopicSerializer, TopicDetailSerializer, EventSerializer,
    WeeklyEditionSerializer, WeeklyArticleSerializer, WeeklyEditionListSerializer,
    SearchSerializer, InDepthProjectListSerializer, InDepthProjectSerializer, ReportDetailSerializer
)
from helpers import get_subpages
from newamericadotorg.settings.context_processors import content_types
from programs.models import Program, Subprogram, AbstractContentPage
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyArticle, WeeklyEdition
from in_depth.models import InDepthProject
from report.models import Report
from custom_contenttype.models import CustomContentTypeCategory
from subscribe.campaign_monitor import update_subscriber

class PostFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    program_id = django_filters.CharFilter(name='parent_programs__id', lookup_expr='iexact')
    subprogram_id = django_filters.CharFilter(name='post_subprogram__id', lookup_expr='iexact')
    author_id = django_filters.CharFilter(name='post_author__id', lookup_expr='iexact')
    author_slug = django_filters.CharFilter(name='post_author__slug', lookup_expr="iexact")
    after = django_filters.DateFilter(name='date', lookup_expr='gte')
    before = django_filters.DateFilter(name='date', lookup_expr='lte')
    content_type = django_filters.CharFilter(name='content_type__model')

    class Meta:
        model = Post
        fields = ['id', 'program_id', 'subprogram_id', 'before', 'after', 'content_type']

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = PostFilter

    def get_queryset(self):
        ids = self.request.query_params.getlist('id[]', None)
        topic_id = self.request.query_params.get('topic_id', None)
        posts = Post.objects.live().order_by('-date').not_type(Event).distinct()
        content_type_id = self.request.query_params.get('content_type_id', None)
        category_id = self.request.query_params.get('category_id', None)

        if topic_id:
            topics = IssueOrTopic.objects.get(pk=topic_id)\
                .get_descendants(inclusive=True).live()

            posts = posts.filter(post_topic__in=topics)

        if ids:
            posts = posts.filter(id__in=ids)

        if content_type_id:
            posts = posts.descendant_of(Page.objects.get(pk=content_type_id))

        if category_id:
            posts = posts.descendant_of(Page.objects.get(pk=category_id))

        return posts;

class ReportDetail(generics.RetrieveAPIView):
    serializer_class = ReportDetailSerializer
    queryset = Report.objects.live()

class SearchList(generics.ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        results = Page.objects.live().search(search)
        query = Query.get(search)
        query.add_hit()
        return results


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

class AuthorFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')
    slug = django_filters.CharFilter(name='slug', lookup_expr="iexact")
    program_id = django_filters.CharFilter(name='belongs_to_these_programs__id', lookup_expr='iexact')
    program_slug = django_filters.CharFilter(name='belongs_to_these_programs__slug', lookup_expr='iexact')
    subprogram_id = django_filters.CharFilter(name='belongs_to_these_subprograms__id', lookup_expr='iexact')
    role = django_filters.CharFilter(name='role', lookup_expr='iexact')
    leadership = django_filters.BooleanFilter(name='leadership')
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
    pagination_class = WeeklyPagination

    def get_queryset(self):
        queryset = WeeklyEdition.objects.live()
        return sorted(queryset, key=lambda edition: get_edition_number(edition));

class WeeklyDetail(generics.RetrieveAPIView):
    queryset = WeeklyEdition.objects.live()
    serializer_class = WeeklyEditionSerializer

class InDepthProjectList(generics.ListAPIView):
    serializer_class = InDepthProjectListSerializer
    queryset = InDepthProject.objects.live().order_by('-date')

class InDepthProjectDetail(generics.RetrieveAPIView):
    queryset = InDepthProject.objects.live()
    serializer_class = InDepthProjectSerializer

class AuthorList(generics.ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = AuthorFilter

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id', None)
        queryset = Person.objects.live().order_by('last_name').filter(former=False).exclude(role__icontains='External Author').distinct()

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
        events = Event.objects.live().distinct()

        if time_period:
            today = localtime(now()).date()
            if time_period=='future':
                return events.filter(Q(date__gte=today)).order_by('date', 'start_time')
            elif time_period=='past':
                return events.filter(date__lt=today).order_by('-date', '-start_time')
        if not ids:
            return events.order_by('-date', '-start_time')

        return events.filter(id__in=ids).order_by('-date', '-start_time')

class MetaList(views.APIView):
    def get(self, request, format=None):
        subpages = get_subpages(HomePage)
        programs = ProgramSerializer(Program.objects.live(), many=True).data
        subprograms = SubprogramSerializer(Subprogram.objects.live(), many=True).data
        home = HomeSerializer(HomePage.objects.live().first()).data

        return response.Response({
            'count': None,
            'next': None,
            'previous': None,
            'results': {
                'subpages': subpages,
                'programs': programs,
                'subprograms': subprograms,
                'home': home
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
    queryset = Program.objects.in_menu().live().order_by('title').exclude(location=True)
    serializer_class = ProgramSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = ProgramFilter

class SubprogramFilter(FilterSet):
    id = django_filters.CharFilter(name='id', lookup_expr='iexact')

    class Meta:
        model = Subprogram
        fields = ['id',]

class SubprogramList(generics.ListAPIView):
    queryset = Subprogram.objects.live().order_by('title')
    serializer_class = SubprogramSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter)
    filter_class = SubprogramFilter

class SubprogramDetail(generics.RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SubprogramSerializer


@api_view(['POST'])
def subscribe(request):
    params = request.data
    subscriptions = params.getlist('subscriptions[]', None)
    job_title = params.get('job_title', None)
    org = params.get('organization', None)
    custom_fields = []

    if job_title:
        custom_fields.append({ 'key': 'JobTitle', 'value': job_title })
    if org:
        custom_fields.append({ 'key': 'Organization', 'value': org })
    if subscriptions:
        for s in subscriptions:
            custom_fields.append({ 'key': 'Subscriptions', 'value': s })

    update_subscriber(params.get('email'), params.get('name'), custom_fields)

    return redirect('/thankyou')
