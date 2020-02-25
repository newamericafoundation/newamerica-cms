from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination

from weekly.models import WeeklyArticle

from .serializers import WeeklyArticleSerializer


class WeeklyPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1000


class WeeklyList(ListAPIView):
    serializer_class = WeeklyArticleSerializer

    def get_queryset(self):
        return WeeklyArticle.objects.live().public()


class WeeklyDetail(RetrieveAPIView):
    serializer_class = WeeklyArticleSerializer

    def get_queryset(self):
        return WeeklyArticle.objects.live().public()
