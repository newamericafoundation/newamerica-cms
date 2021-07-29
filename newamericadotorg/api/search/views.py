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

import survey.models
from .serializers import SearchSerializer
from newamericadotorg.api.event.serializers import EventSerializer
from article.models import Article
from book.models import Book
from brief.models import Brief
from press_release.models import PressRelease
from event.models import Event
from weekly.models import WeeklyArticle
from blog.models import BlogPost
from the_thread.models import ThreadArticle
from podcast.models import Podcast
from quoted.models import Quoted
from policy_paper.models import PolicyPaper
from in_depth.models import InDepthProject
from other_content.models import OtherPost
from programs.models import Program, Subprogram
from home.models import Post, RedirectPage
from person.models import Person
from subscribe.models import SubscriptionSegment
from report.models import Report


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
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        site_for_request = Site.find_for_request(self.request)
        results = exclude_invisible_pages(
            self.request,
            Page.objects.live().descendant_of(
                site_for_request.root_page, inclusive=True
            ),
        )

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

        base_query = (
            Page.objects.live()
            .public()
            .type((Program, Subprogram))
            .descendant_of(site_for_request.root_page, inclusive=True)
        )
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
        site_for_request = Site.find_for_request(self.request)

        base_query = (
            Person.objects.live()
            .filter(former=False)
            .public()
            .descendant_of(site_for_request.root_page, inclusive=True)
        )
        qs = exclude_invisible_pages(self.request, base_query)

        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs


class SearchOtherPages(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        site_for_request = Site.find_for_request(self.request)

        base_query = (
            Page.objects.live()
            .public()
            .not_type(
                (
                    # Pages included in other searches
                    Person,
                    Program,
                    Subprogram,
                    Event,
                    SubscriptionSegment,
                    RedirectPage,
                    # Exclude all Post subclasses except "Survey"
                    Article,
                    Book,
                    Brief,
                    PressRelease,
                    Event,
                    WeeklyArticle,
                    BlogPost,
                    ThreadArticle,
                    Podcast,
                    Quoted,
                    PolicyPaper,
                    InDepthProject,
                    OtherPost,
                    Report,
                    # Non-informational pages for survey filtering.
                    survey.models.SurveyOrganization,
                    survey.models.DemographicKey,
                    survey.models.SurveyTags,
                    survey.models.SurveyValuesIndex,
                )
            )
            .descendant_of(site_for_request.root_page, inclusive=True)
        )
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
        site_for_request = Site.find_for_request(self.request)
        today = localtime(now()).date()

        base_query = (
            Event.objects.live()
            .public()
            .filter(date__gte=today)
            .descendant_of(site_for_request.root_page, inclusive=True)
        )
        qs = exclude_invisible_pages(self.request, base_query)
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
        site_for_request = Site.find_for_request(self.request)
        today = localtime(now()).date()

        base_query = (
            Post.objects.live()
            .public()
            .type((Post, Event))
            .not_type(survey.models.Survey)
            .filter(date__lt=today)
            .descendant_of(site_for_request.root_page, inclusive=True)
        )
        qs = exclude_invisible_pages(self.request, base_query)
        if search:
            qs = qs.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()
        return qs
