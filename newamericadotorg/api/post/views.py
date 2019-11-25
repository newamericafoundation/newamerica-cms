from django_filters import CharFilter, DateFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import CursorPagination

from wagtail.core.models import Page

from home.models import Post
from other_content.models import OtherPost
from issue.models import IssueOrTopic
from event.models import Event

from .serializers import PostSerializer


class PostCursorPagination(CursorPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 200
    ordering = '-first_published_at'


class PostFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='iexact')
    program_id = CharFilter(field_name='parent_programs__id', lookup_expr='iexact')
    subprogram_id = CharFilter(field_name='post_subprogram__id', lookup_expr='iexact')
    author_id = CharFilter(field_name='post_author__id', lookup_expr='iexact')
    author_slug = CharFilter(field_name='post_author__slug', lookup_expr="iexact")
    after = DateFilter(field_name='date', lookup_expr='gte')
    before = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['id', 'program_id', 'subprogram_id', 'before', 'after']


class PostList(ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)
    filter_class = PostFilter
    pagination_class = PostCursorPagination

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type', None)
        other_content_type_title = self.request.query_params.get('other_content_type_title', None)
        topic_id = self.request.query_params.get('topic_id', None)
        category = self.request.query_params.get('category', None)

        if other_content_type_title:
            posts = OtherPost.objects.live().public()\
                .filter(other_content_type__title=other_content_type_title)
            if category:
                posts = posts.filter(category__title=category)
        else:
            posts = Post.objects.live().not_type(Event).public()

        if content_type:
            if content_type == 'report':
                posts = posts.filter(content_type__model__in=['report', 'policypaper', 'indepthproject'])
            else:
                posts = posts.filter(content_type__model=content_type)

        if topic_id:
            try:
                topics = IssueOrTopic.objects.get(pk=topic_id)\
                    .get_descendants(inclusive=True).live()

                posts = posts.filter(post_topic__id__in=[t.id for t in topics])
            except:
                return posts.none()

        return posts.distinct()
