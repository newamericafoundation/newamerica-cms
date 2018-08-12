from django.db.models import Q
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        program_id = self.request.query_params.get('program_id', None)
        subprogram_id = self.request.query_params.get('subprogram_id', None)
        context['program_id'] = program_id
        context['subprogram_id'] = subprogram_id

        return context

    def get_queryset(self):
        queryset = Person.objects.live().order_by('sort_priority', 'last_name')\
            .exclude(role__icontains='External Author')
        topic_id = self.request.query_params.get('topic_id', None)
        program_id = self.request.query_params.get('program_id', None)
        subprogram_id = self.request.query_params.get('subprogram_id', None)
        former = strtobool(self.request.query_params.get('former', 'false'))
        include_fellows = strtobool(self.request.query_params.get('include_fellows', 'false'))

        if not include_fellows:
            if program_id:
                queryset = queryset.exclude(
                    Q(role__icontains='fellow') |
                    Q(programs__program__id=program_id, programs__group__in=['Current Fellows', 'Former Fellows'])
                )
            elif subprogram_id:
                queryset = queryset.exclude(
                    Q(role__icontains='fellow') |
                    Q(subprograms__subprogram__id=subprogram_id, subprograms__group__in=['Current Fellows', 'Former Fellows'])
                )
            else:
                queryset = queryset.exclude(
                    Q(role__icontains='fellow') |
                    Q(programs__group='Current Fellows') |
                    Q(subprograms__group='Current Fellows')
                )

        queryset = queryset.filter(former=former)

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        program_id = self.request.query_params.get('program_id', None)
        subprogram_id = self.request.query_params.get('subprogram_id', None)
        context['program_id'] = program_id
        context['subprogram_id'] = subprogram_id

        return context

    def get_queryset(self):
        queryset = Person.objects.live().order_by('sort_priority', 'last_name')
        program_id = self.request.query_params.get('program_id', None)
        subprogram_id = self.request.query_params.get('subprogram_id', None)
        topic_id = self.request.query_params.get('topic_id', None)
        former = strtobool(self.request.query_params.get('former', 'false'))
        rel_former = 'Former Fellows' if former else 'Current Fellows'

        if program_id:
            queryset = queryset.filter(
                Q(former=former, role__icontains='fellow'),
                ~Q(programs__group__in=['Current Fellows', 'Former Fellows'], programs__program__id=program_id) |
                Q(programs__group=rel_former, programs__program__id=program_id)
            )
        elif subprogram_id:
            queryset = queryset.filter(
                Q(former=former, role__icontains='fellow'),
                ~Q(subprograms__group__in=['Current Fellows', 'Former Fellows'], subprograms__subprogram__id=subprogram_id) |
                Q(subprograms__group=rel_former, subprograms__subprogram__id=subprogram_id)
            )
        else:
            queryset = queryset.filter(
                Q(former=former, role__icontains='fellow'),
                ~Q(programs__group__in=['Current Fellows', 'Former Fellows']),
                ~Q(subprograms__group__in=['Current Fellows', 'Former Fellows']) |
                Q(subprograms__group=rel_former) | Q(programs__group=rel_former)
            )

        if topic_id:
            try:
                topics = IssueOrTopic.objects.get(pk=topic_id)\
                    .get_descendants(inclusive=True).live()

                queryset = queryset.filter(expertise__in=[t.id for t in topics])
            except:
                return queryset.none()

        return queryset.distinct()
