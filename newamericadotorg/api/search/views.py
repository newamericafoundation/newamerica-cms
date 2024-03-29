from django.utils.timezone import localtime, now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page, PageViewRestriction, Site

import survey.models
from article.models import Article
from blog.models import BlogPost
from book.models import Book
from brief.models import Brief
from event.models import Event
from home.models import Post, RedirectPage
from in_depth.models import InDepthProject
from other_content.models import OtherPost
from person.models import Person
from podcast.models import Podcast
from policy_paper.models import PolicyPaper
from press_release.models import PressRelease
from programs.models import Program, Subprogram
from quoted.models import Quoted
from report.models import Report
from the_thread.models import ThreadArticle
from weekly.models import WeeklyArticle

from .serializers import SearchSerializer


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
