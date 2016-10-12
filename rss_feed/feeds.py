from django.db import models
from django.contrib.syndication.views import Feed
from django.http import Http404
from wagtail.wagtailcore.models import Page

from home.models import Post

# "issueortopic", "quoted","weeklyedition", "indepthproject"
acceptable_content_types = [
    None, "program","subprogram","person","book","article","blogpost",
    "event","podcast","policypaper","pressrelease",
    "weeklyarticle","indepthsection",
]

#"fellows","new-america-weekly",
acceptable_programs = [
    "asset-building","better-life-lab","cybersecurity-initiative",
    "economic-growth","education-policy","future-tense",
    "international-security","open-technology-institute",
    "political-reform","open-markets","resilient-communities",
    "opportunity-at-work",
]

class PostsFeed(Feed):

    def get_object(self, request, content_type=None, programorauthor=None):
        if content_type not in acceptable_content_types:
            raise Http404

        # content_type, author, program, and subprogram serve as filters
        # page gives title, description, and link to homepage
        obj = {
            "content_type": content_type,
            "program": programorauthor,
            "subprogram": None,
            "author": None,
            "page": None
        }

        # do not filter by program when filtering by author
        if content_type == "person":
            obj["author"] = programorauthor
            obj["program"] = None
            obj["page"] = Page.objects.live().filter(content_type__model="person",slug=programorauthor).first()
        # filter for all content types when filtering by program
        # throw 404 if not in program list
        elif content_type == "program":
            if programorauthor not in acceptable_programs:
                raise Http404
            obj["content_type"] = None
            obj["page"] = Page.objects.live().filter(content_type__model="program",slug=programorauthor).first()
        # filter for all content types and programs when filtering by subprogram
        elif content_type == "subprogram":
            obj["content_type"] = None
            obj["program"] = None
            obj["subprogram"] = programorauthor
            obj["page"] = Page.objects.live().filter(content_type__model="subprogram",slug=programorauthor).first()
        else:
            if content_type == "indepthsection":
                obj["page"] = Page.objects.live().filter(content_type__model="allindepthhomepage").first()
            elif content_type == "weeklyarticle":
                obj["page"] = Page.objects.live().filter(content_type__model="weekly").first()
            else:
                obj["page"] = Page.objects.live().filter(content_type__model="all"+content_type+"shomepage").first()

        return obj

    def title(self, obj):
        return obj["page"].title

    def description(self, obj):
        return obj["page"].search_description

    def link(self, obj):
        return obj["page"].full_url

    def items(self, obj):
        # get everything then pare it down. Performant?
        posts = Post.objects.live().order_by('-date')

        # apply applicable filters and return the first 10 results
        if obj["content_type"] is not None:
            posts = posts.filter(content_type__model=obj["content_type"])

        if obj["program"] is not None:
            return posts.filter(parent_programs__slug=obj["program"])[:10]
        elif obj["subprogram"] is not None:
            return posts.filter(subprogram__slug=obj["subprogram"])[:10]
        elif obj["author"] is not None:
            return posts.filter(post_author__slug=obj["author"])[:10]
        else:
            return posts[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.search_description

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, item):
        return item.first_published_at
