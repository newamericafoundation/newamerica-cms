from distutils.util import strtobool
from django_filters import CharFilter, TypedChoiceFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from issue.models import IssueOrTopic
from person.models import Person

from .serializers import AuthorSerializer

BOOLEAN_CHOICES = (('false', 'False'), ('true', 'True'),)

class AuthorFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='iexact')
    slug = CharFilter(field_name='slug', lookup_expr="iexact")
    program_id = CharFilter(field_name='belongs_to_these_programs__id', lookup_expr='iexact')
    program_slug = CharFilter(field_name='belongs_to_these_programs__slug', lookup_expr='iexact')
    subprogram_id = CharFilter(field_name='belongs_to_these_subprograms__id', lookup_expr='iexact')
    role = CharFilter(field_name='role', lookup_expr='iexact')
    leadership = TypedChoiceFilter(choices=BOOLEAN_CHOICES,coerce=strtobool)
    name = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = ['id','program_id', 'subprogram_id', 'name', 'role', 'leadership']

class AuthorList(ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = AuthorFilter

    def get_queryset(self):
        queryset = Person.objects.live().order_by('sort_priority', 'last_name')\
            .exclude(role__icontains='External Author')
        topic_id = self.request.query_params.get('topic_id', None)
        former = self.request.query_params.get('former', 'false')
        include_fellows = self.request.query_params.get('include_fellows', None)

        if not include_fellows or include_fellows == 'false':
            queryset = queryset.exclude(role__icontains='fellow')

        if former == 'false':
            queryset = queryset.filter(former=False)
        elif former == 'true':
            queryset = queryset.filter(former=True)

        if topic_id is not None:
            # rollup topic tags
            try:
                topics = IssueOrTopic.objects.get(pk=topic_id)\
                    .get_descendants(inclusive=True).live()

                queryset = queryset.filter(expertise__in=[t.id for t in topics])
            except:
                return queryset.none()


        return queryset.distinct()

class FellowList(ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = AuthorFilter

    def get_queryset(self):
        queryset = Person.objects.live().order_by('fellowship_year', 'sort_priority', 'last_name').filter(role='Fellow')
        fellowship_year = self.request.query_params.get('fellowship_year', None)
        topic_id = self.request.query_params.get('topic_id', None)
        former = self.request.query_params.get('former', 'false')

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
            try:
                topics = IssueOrTopic.objects.get(pk=topic_id)\
                    .get_descendants(inclusive=True).live()

                queryset = queryset.filter(expertise__in=[t.id for t in topics])
            except:
                return queryset.none()

        return queryset.distinct()
