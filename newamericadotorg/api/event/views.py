from django.utils.timezone import localtime, now
from django.db.models import Q
from django_filters import CharFilter, DateFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from home.models import Post
from event.models import Event

from .serializers import EventSerializer

class EventFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='iexact')
    program_id = CharFilter(field_name='parent_programs__id', lookup_expr='iexact')
    subprogram_id = CharFilter(field_name='post_subprogram__id', lookup_expr='iexact')
    program_slug = CharFilter(field_name='parent_programs__slug', lookup_expr='iexact')
    subprogram_slug = CharFilter(field_name='post_subprogram__slug', lookup_expr='iexact')
    topic_id = CharFilter(field_name='topic__id', lookup_expr='iexact')
    after = DateFilter(field_name='date', lookup_expr='gte')
    before = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['id', 'program_id', 'subprogram_id', 'before', 'after', 'topic_id']

class EventList(ListAPIView):
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = EventFilter

    def get_queryset(self):
        time_period = self.request.query_params.get('time_period', None)
        events = Event.objects.live().public().distinct()

        if time_period:
            today = localtime(now()).date()
            if time_period=='future':
                return events.filter(Q(date__gte=today)).order_by('date', 'start_time')
            elif time_period=='past':
                return events.filter(date__lt=today).order_by('-date', '-start_time')

        return events.order_by('-date', '-start_time')
