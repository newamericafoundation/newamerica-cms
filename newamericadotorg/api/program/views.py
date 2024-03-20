from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from programs.models import (
    FeaturedProgramPage,
    Program,
    Subprogram,
)

from .serializers import (
    FeaturedPageSerializer,
    ProgramDetailSerializer,
    ProgramSerializer,
    ProgramSubprogramSerializer,
    SubprogramSerializer,
)


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
    filterset_class = ProgramFilter

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
    serializer_class = ProgramSubprogramSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filterset_class = SubprogramFilter

class SubprogramDetail(RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SubprogramSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_simple'] = self.request.query_params.get('simple', False)

        return context

class ProgramFeaturedPageList(ListAPIView):
    serializer_class = FeaturedPageSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ['sort_order']

    def get_queryset(self):
        return FeaturedProgramPage.objects.filter(program__id=self.kwargs['pk'])
