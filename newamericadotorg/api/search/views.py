from wagtail.search.backends.elasticsearch2 import Elasticsearch2SearchResults

from django.utils.timezone import localtime, now
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import DateFilter
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from wagtail.core.models import Page, PageViewRestriction, Site
from wagtail.search.models import Query
from wagtail.search.backends import get_search_backend

from .serializers import SearchSerializer
from newamericadotorg.api.event.serializers import EventSerializer
from event.models import Event
from programs.models import Program, Subprogram
from home.models import Post, RedirectPage
from person.models import Person
from subscribe.models import SubscriptionSegment


class ZQuery(object):
    def __init__(self, search_query, programs, content_types):
        self.search_query = search_query
        self.programs = programs
        # self.campaigns = campaigns
        # self.languages = languages
        # self.countries = countries
        self.content_types = content_types

    @property
    def queryset(self):
        # Just has to return any queryset of Page
        # This is used by ElasticSearchResults to find the model to return
        return Page.objects.all()

    def get_query(self):
        # It chokes on empty lists and strings

        # Search query
        if self.search_query:
            query = {
                'multi_match': {
                    'query': self.search_query,
                    'fields': ['_all', '_partials'],
                }
            }
        else:
            query = {
                'match_all': {}
            }

        filters = [
            # {
            #     "prefix": {
            #         "content_type": "wagtailcore_page"
            #         # To filter by content type: append _myapp_mymodel to page
            #     },
            # },
            {
                "term": {
                    "live_filter": True
                }
            },
         ]

        taxonomy_filters = []
        # if self.programs:
        #     taxonomy_filters.append({'terms': {'program_snippets_filter': self.programs}})
        if self.content_types:
            for content_type in self.content_types:
                taxonomy_filters.append({"prefix": {"content_type": "wagtailcore_page_" + content_type}})
        else:
            filters.append({"prefix": {"content_type": "wagtailcore_page"}})

        if taxonomy_filters:
            filters.append({"or": taxonomy_filters})

        f = {
            "filtered": {
                "query": query,
                "filter": {
                    "and": filters
                }
            }
        }
        print(f)
        return f

    def get_sort(self):
        return
        # Ordering by relevance is the default in Elasticsearch
        # if self.order_by_relevance:
        #     return

def exclude_invisible_pages(request, pages):
    # Get list of pages that are restricted to this user
    restricted_pages = [
        restriction.page
        for restriction in PageViewRestriction.objects.all().select_related('page')
        if not restriction.accept_request(request)
    ]

    # Exclude the restricted pages and their descendants from the queryset
    for restricted_page in restricted_pages:
        pages = pages.not_descendant_of(restricted_page, inclusive=True)

    return pages


class SearchList(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        site_for_request = Site.find_for_request(self.request)
        results = exclude_invisible_pages(self.request, Page.objects.live().descendant_of(site_for_request.root_page, inclusive=True))

        if search:
            results = results.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()

        return results


class SearchPrograms(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        site_for_request = Site.find_for_request(self.request)

        base_query = Page.objects.live().public().type(
            (Program, Subprogram),
        ).descendant_of(site_for_request.root_page, inclusive=True)
        qs = exclude_invisible_pages(self.request, base_query)

        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs


class SearchPeople(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)

        # phase 1: fully custom query
        # s = get_search_backend()
        # return Elasticsearch2SearchResults(s, ZQuery(search, '1616', None)) #'person_person'))

        # phase 2: hard code the results
        # return Person.objects.filter(id__in=[459, 575, 7626, 11884, 13911]).search(search, partial_match=True)

        site_for_request = Site.find_for_request(self.request)
        program_id = self.request.query_params.get('program_id', None)
        subprogram_id = self.request.query_params.get('subprogram_id', None)

        base_query = Person.objects.live().public().descendant_of(
            site_for_request.root_page,
            inclusive=True,
        )

        qs = exclude_invisible_pages(self.request, base_query)
        # ids = qs.values_list('id', flat=True)

        # print('got ids', list(ids))
        # qs2 = Person.objects.filter(id__in=list(ids))
        # print('count of person w/ids', ids.count())

        if search:
            print(f'searching with `{search}`, subprogram_id={subprogram_id}, program_id={program_id}')
            if program_id:
                qs._filter_program_id = program_id
            if subprogram_id:
                qs._filter_subprogram_id = subprogram_id
            qs = qs.search(search, partial_match=False)
            # #s = get_search_backend()
            # #qs2 = s.search(search, qs2, partial_match=True)
            # qs2 = qs2.search(search, partial_match=False)
            # print('*' * 79)
            # print('final qs', qs2, qs2.count())
            # print('*' * 79)
            query = Query.get(search)
            query.add_hit()
        return qs


class SearchOtherPages(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        site_for_request = Site.find_for_request(self.request)

        program_id = self.request.query_params.get('program_id')
        subprogram_id = self.request.query_params.get('subprogram_id')
        if program_id:
            search_root = Program.objects.get(pk=program_id)
        elif subprogram_id:
            search_root = Subprogram.objects.get(pk=subprogram_id)
        else:
            search_root = site_for_request.root_page

        base_query = Page.objects.live().public().not_type(
            (Person, Program, Subprogram, Post, Event, SubscriptionSegment, RedirectPage),
        ).descendant_of(search_root, inclusive=True)
        qs = exclude_invisible_pages(self.request, base_query)

        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs


class SearchUpcomingEvents(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        program_id = self.request.query_params.get('program_id')
        subprogram_id = self.request.query_params.get('subprogram_id')
        site_for_request = Site.find_for_request(self.request)
        today = localtime(now()).date()

        search_root = site_for_request.root_page

        base_query = Event.objects.live().public().filter(
            date__gte=today
        ).descendant_of(search_root, inclusive=True)
        qs = exclude_invisible_pages(self.request, base_query)

        if program_id:
            qs._filter_post__program_id = program_id
        if subprogram_id:
            qs._filter_post__subprogram_id = subprogram_id

        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs


class SearchPublicationsAndPastEvents(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        program_id = self.request.query_params.get('program_id')
        subprogram_id = self.request.query_params.get('subprogram_id')
        site_for_request = Site.find_for_request(self.request)
        today = localtime(now()).date()

        base_query = Post.objects.live().public().type(
            (Post, Event),
        ).filter(date__lt=today).descendant_of(
            site_for_request.root_page,
            inclusive=True,
        )
        qs = exclude_invisible_pages(self.request, base_query)

        if program_id:
            qs._filter_post__program_id = program_id
        if subprogram_id:
            qs._filter_post__subprogram_id = subprogram_id

        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs
