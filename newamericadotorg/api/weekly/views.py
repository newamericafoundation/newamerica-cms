from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import CursorPagination

from weekly.models import WeeklyArticle

from .serializers import DetailWeeklyArticleSerializer, ListingWeeklyArticleSerializer


class WeeklyCursorPagination(CursorPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 200
    ordering = '-ordered_date_string'


class WeeklyList(ListAPIView):
    serializer_class = ListingWeeklyArticleSerializer
    pagination_class = WeeklyCursorPagination

    def get_queryset(self):
        return WeeklyArticle.objects.live().public().prefetch_related('authors__author__profile_image').select_related('story_image')


class WeeklyDetail(RetrieveAPIView):
    serializer_class = DetailWeeklyArticleSerializer

    def get_queryset(self):
        return WeeklyArticle.objects.live().public()
