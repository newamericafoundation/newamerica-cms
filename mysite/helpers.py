from programs.models import Program, Subprogram
from mysite.pagination import paginate_results


def get_posts_and_programs(self, request, page_type, content_model):
    """
    Function to return a list of content for a program or 
    subprogram content homepage
    """
    context = super(page_type, self).get_context(request)
    
    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)
        all_posts = content_model.objects.filter(parent_programs=program).order_by("-date")
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)
        all_posts = content_model.objects.filter(post_subprogram=program).order_by("-date")
    
    context['all_posts'] = paginate_results(request, all_posts)

    context['program'] = program
    
    return context