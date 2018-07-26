from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination

from weekly.models import WeeklyEdition

from .serializers import WeeklyEditionSerializer, WeeklyEditionListSerializer

class WeeklyPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000

class WeeklyList(ListAPIView):
    serializer_class = WeeklyEditionListSerializer

    def get_queryset(self):
        queryset = WeeklyEdition.objects.live().public()
        return sorted(queryset, key=lambda edition: get_edition_number(edition));

class WeeklyDetail(RetrieveAPIView):
    queryset = WeeklyEdition.objects.all()
    serializer_class = WeeklyEditionSerializer

def get_edition_number(edition):
    if 'edition-' in edition.slug:
        return -int(edition.slug.split('-')[1])
    return -int(edition.slug)
