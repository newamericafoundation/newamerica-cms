import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict

from django.db.models import Q

from programs.models import Program, Subprogram

def is_int(n):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_json(v):
    try:
        json.loads(date)
        return True
    except ValueError:
        return False

def paginate_results(request, all_posts):
    page = request.GET.get('page')
    paginator = Paginator(all_posts, 12)

    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return all_posts


def get_org_wide_posts(self, request, page_type, content_model):
    """
    Function to return a list of content
    for org wide content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(page_type, self).get_context(request)

    search_program = request.GET.get('program_id', None)
    date = request.GET.get('date', None)

    filter_dict = {}

    if search_program:
        if is_int(search_program):
            filter_dict['parent_programs'] = int(search_program)
    if date:
        if is_json(date):
            date_range = json.loads(date)
            filter_dict['date__range'] = (date_range['start'], date_range['end'])

    all_posts = content_model.objects.filter(**filter_dict)
    context['all_posts'] = paginate_results(request, all_posts.live().order_by("-date"))
    context['programs'] = Program.objects.filter(Q(live=True), Q(show_in_menus=True)| Q(location=True)).order_by('title')
    context['query_url'] = generate_url(request)

    return context


def get_program_and_subprogram_posts(self, request, page_type, content_model):
    """
    Function to return a list of content for a program or
    subprogram content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(page_type, self).get_context(request)

    search_subprogram = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)

    filter_dict = {}
    # if program
    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)

        filter_dict['parent_programs'] = program
        if search_subprogram:
            filter_dict['post_subprogram'] = int(search_subprogram)

        context['subprograms'] = program.get_children().type(Subprogram).live().order_by('title')
    # if subprogram
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)
        filter_dict['post_subprogram'] = program

    if date:
        if is_json(date):
            date_range = json.loads(date)
            filter_dict['date__range'] = (date_range['start'], date_range['end'])

    all_posts = content_model.objects.live().filter(**filter_dict)
    context['all_posts'] = paginate_results(request, all_posts.order_by("-date"))
    context['query_url'] = generate_url(request)
    context['program'] = program

    return context

def generate_url(request):
    query = QueryDict(mutable=True)
    program_id = request.GET.get("program_id", None)
    subprogram_id = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)
    if program_id:
        query['program_id'] = program_id
    if date:
        query['date'] = date
    if subprogram_id:
        query['subprogram_id'] = subprogram_id

    return query.urlencode()
