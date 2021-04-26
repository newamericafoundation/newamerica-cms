from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import CursorPagination

from the_thread.models import ThreadArticle

from .serializers import DetailThreadArticleSerializer, ListingThreadArticleSerializer


class ThreadCursorPagination(CursorPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 200
    ordering = '-ordered_date_string'


class ThreadList(ListAPIView):
    serializer_class = ListingThreadArticleSerializer
    pagination_class = ThreadCursorPagination

    def get_queryset(self):
        return ThreadArticle.objects.live().public().prefetch_related('authors__author__profile_image').select_related('story_image')


class ThreadDetail(RetrieveAPIView):
    serializer_class = DetailThreadArticleSerializer

    def get_queryset(self):
        return ThreadArticle.objects.live().public()
