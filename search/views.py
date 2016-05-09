from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from programs.models import Program

from home.models import Post

import os

def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)
    search_program = request.GET.get('program_id', None)
    programs = Program.objects.all().order_by('title')

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })


def search404(request):
    print(request.path)

    search_query = os.path.basename(os.path.normpath(request.path))
    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

   

    return render(request, '404.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
