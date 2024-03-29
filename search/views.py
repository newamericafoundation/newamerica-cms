import os

from django.shortcuts import render
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query", None)

    return render(
        request,
        "search/search.html",
        {
            "search_query": search_query,
        },
    )


# retrieves final segment of url path from request and initiates search based on this segment as the query
#   - handles urls with final slash and without, ignores parameters


def search404(request):
    search_query = os.path.basename(os.path.normpath(request.path))
    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    return render(
        request,
        "404.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
