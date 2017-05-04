from home.models import Post, HomePage
from programs.models import Program, Subprogram

def meta(request):
    program_data = {}
    programs = Program.objects.live()

    for prog in programs:
        d = program_data[prog.title] = {
            'id': prog.id,
            'title': prog.title,
            'url': prog.url,
            'slug': prog.slug
        }
        pages = prog.get_children().live()
        for p in pages:
            m = p.content_type.model
            if not getattr(d, m+'s', None):
                d[m+'s'] = []
            d[m+'s'].append({
                'id': p.id,
                'title': p.title,
                'url': p.url,
                'slug': p.slug
            })

    return program_data
