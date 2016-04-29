import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from programs.models import Program, Subprogram

def paginate_results(request, all_posts):
    page = request.GET.get('page')
    paginator = Paginator(all_posts, 10)
    
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return all_posts


def get_posts_and_programs(self, request, page_type, content_model):
    """
    Function to return a list of content for a program or 
    subprogram content homepage
    """
    context = super(page_type, self).get_context(request)

    page = request.GET.get('page', 1)
    search_subprogram = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)

    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)

        filter_dict = {'parent_programs': program}
        if search_subprogram:
            filter_dict['post_subprogram'] = int(search_subprogram)
        if date:
            date_range = json.loads(date)
            filter_dict['date__range'] = (date_range['start'], date_range['end'])
    
        all_posts = content_model.objects.filter(**filter_dict)
        context['subprograms'] = program.get_children().type(Subprogram)
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)
        all_posts = content_model.objects.filter(post_subprogram=program)

    context['all_posts'] = paginate_results(request, all_posts.order_by("-date"))

    context['program'] = program
    print(all_posts.filter(post_subprogram=program.get_children().type(Subprogram)))
    
    return context