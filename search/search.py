from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from programs.models import Program


def content_search(request, search_model, context):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('query', None)
    search_program = request.GET.get('program',)

    # Search
    if search_query:
        if search_program:
            program = Program.objects.get(title=search_program)
            search_results = search_model.objects.filter(belongs_to_these_programs=program).live().search(search_query)
        else:
            search_results = search_model.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = search_model.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)


    context['search_query'] = search_query
    context['search_results'] = search_results
    
    return context