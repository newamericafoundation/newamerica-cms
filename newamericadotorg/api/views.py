import django_filters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from home.models import Post, HomePage
from person.models import Person
from serializers import PostSerializer, AuthorSerializer, ProgramSerializer, SubprogramSerializer, HomeSerializer
from helpers import get_content_types
from programs.models import Program, Subprogram
from rest_framework import mixins

class PostFilter(django_filters.rest_framework.FilterSet):
    program = django_filters.CharFilter(name='parent_programs__name', lookup_expr='iexact')
    subprogram = django_filters.CharFilter(name='post_subprogram__name', lookup_expr='iexact')
    after = django_filters.DateFilter(name='date', lookup_expr='gte')
    before = django_filters.DateFilter(name='date', lookup_expr='lte')
    content_type = django_filters.CharFilter(name='content_type__model')

    class Meta:
        model = Post
        fields = ['program', 'subprogram', 'before', 'after', 'content_type']

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PostFilter

    def get_queryset(self):
        ids = self.request.query_params.getlist('id[]', None)

        if not ids:
            return Post.objects.live()

        return Post.objects.live().filter(id__in=ids)

class AuthorFilter(django_filters.rest_framework.FilterSet):
    program = django_filters.CharFilter(name='belongs_to_these_programs__name', lookup_expr='iexact')
    subprogram = django_filters.CharFilter(name='belongs_to_these_subprograms__name', lookup_expr='iexact')
    name = django_filters.CharFilter(name='title', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = ['program', 'subprogram', 'role', 'name']

class AuthorList(generics.ListAPIView):
    queryset = Person.objects.live()
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = AuthorFilter

class MetaView(APIView):
    def get(self, request, format=None):
        content_types = get_content_types(HomePage)
        programs = ProgramSerializer(Program.objects.live(), many=True).data
        subprograms = SubprogramSerializer(Subprogram.objects.live(), many=True).data
        home = HomeSerializer(HomePage.objects.live().first()).data

        return Response({
            'content_types': content_types,
            'programs': programs,
            'subprograms': subprograms,
            'home': home
        })

class ContentList(APIView):
    def get(self, request, format=None):
        content_types = get_content_types()
        return Response(content_types)

class ProgramList(generics.ListAPIView):
    queryset = Program.objects.live()
    serializer_class = ProgramSerializer

class SubprogramList(generics.ListAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SubprogramSerializer
