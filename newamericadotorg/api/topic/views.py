from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters import CharFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from issue.models import IssueOrTopic

from .serializers import TopicSerializer, TopicDetailSerializer

class TopicFilter(FilterSet):
    program_id = CharFilter(field_name='parent_program__id', lookup_expr='iexact')

    class Meta:
        model = IssueOrTopic
        fields = ['program_id']

class TopicList(ListAPIView):
    serializer_class = TopicSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TopicFilter
    queryset = IssueOrTopic.objects.live().filter(depth=5)

class TopicDetail(RetrieveAPIView):
    serializer_class = TopicDetailSerializer
    queryset = IssueOrTopic.objects.live()
