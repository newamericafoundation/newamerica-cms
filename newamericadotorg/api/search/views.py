from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from wagtail.core.models import Page, PageViewRestriction
from wagtail.search.models import Query

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
    filter_backends = (DjangoFilterBackend,SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        results = exclude_invisible_pages(self.request, Page.objects.live())

        if search:
            results = results.search(search, partial_match=False)
            query = Query.get(search)
            query.add_hit()

        return results
