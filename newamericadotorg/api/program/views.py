from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters import CharFilter
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.filters import SearchFilter

from programs.models import Program, Subprogram

from .serializers import ProgramSerializer, SubprogramSerializer, ProgramDetailSerializer

class ProgramFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='iexact')
    slug = CharFilter(field_name='slug', lookup_expr='iexact')

    class Meta:
        model = Program
        fields = ['id', 'slug']

class ProgramDetail(RetrieveAPIView):
    queryset = Program.objects.live()
    serializer_class = ProgramDetailSerializer

class ProgramList(ListAPIView):
    serializer_class = ProgramSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = ProgramFilter

    def get_queryset(self):
        return Program.objects.in_menu().live().public().order_by('title').exclude(location=True)

class SubprogramFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='iexact')
    program_id = CharFilter(field_name='parent_programs__id', lookup_expr='iexact')

    class Meta:
        model = Subprogram
        fields = ['id', 'program_id']

class SubprogramList(ListAPIView):
    queryset = Subprogram.objects.live().order_by('title')
    serializer_class = SubprogramSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = SubprogramFilter

class SubprogramDetail(RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SubprogramSerializer
