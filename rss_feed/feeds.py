from django.db import models
from django.contrib.syndication.views import Feed
from django.http import Http404
from wagtail.wagtailcore.models import Page

from home.models import Post
from person.models import Person
from programs.models import Program, Subprogram

# "issueortopic", "quoted","weeklyedition", "indepthproject"
acceptable_content_types = [
    "book","article","blogpost",
    "event","podcast","policypaper","pressrelease",
    "weeklyarticle","indepthsection",
]

programs = Program.objects.live()
acceptable_programs = [p.slug for p in programs]

class GenericFeed(Feed):
    def get_object(self,request):
        return {
            # page data is used for title, description and link tags at top level of rss channel
            "page": Page.objects.live().filter(content_type__model="homepage").first()
        }

    def title(self, obj):
        if obj["page"]:
            return obj["page"].title
        else:
            raise Http404

    def description(self, obj):
        if obj["page"]:
            return obj["page"].search_description
        else:
            raise Http404

    def link(self, obj):
        if obj["page"]:
            return obj["page"].full_url
        else:
            raise Http404

    def items(self, obj):
        return Post.objects.live().order_by("-date")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.story_excerpt

    def item_pubdate(self, item):
        return item.first_published_at

    def item_link(self, item):
        return item.full_url

class ProgramFeed(GenericFeed):
    def get_object(self, request, program):
        return {
            "program": program,
            "page": Program.objects.live().filter(slug=program).first()
        }

    def description(self, obj):
        if obj["page"]:
            return obj["page"].description
        else:
            raise Http404

    def items(self, obj):
        return Post.objects.live().filter(parent_programs__slug=obj["program"]).order_by("-date")[:10]

class SubprogramFeed(GenericFeed):
    def get_object(self, request, subprogram):
        return {
            "subprogram": subprogram,
            "page": Subprogram.objects.live().filter(slug=subprogram).first()
        }

    def description(self, obj):
        if obj["page"]:
            return obj["page"].description
        else:
            raise Http404

    def items(self, obj):
        return Post.objects.live().filter(post_subprogram__slug=obj["subprogram"]).order_by("-date")[:10]

class AuthorFeed(GenericFeed):
    def get_object(self, request, author):
        return {
            "author": author,
            "page": Person.objects.live().filter(slug=author).first()
        }

    def description(self, obj):
        if obj["page"]:
            return obj["page"].short_bio
        else:
            raise Http404

    def items(self, obj):
        return Post.objects.live().filter(post_author__slug=obj["author"]).order_by("-date")[:10]

class ContentFeed(GenericFeed):
    def get_object(self, request, content_type, program=None):
        if content_type not in acceptable_content_types:
            raise Http404

        # page exceptions for indepth and weekly content types
        if content_type == "indepthsection":
            content_type_model = "allindepthhomepage"
        elif content_type == "weeklyarticle":
            content_type_model = "weekly"
        else:
            content_type_model = "all"+content_type+"shomepage"

        return {
            "content_type": content_type,
            "program": program,
            "page": Page.objects.live().filter(content_type__model=content_type_model).first()
        }

    def items(self, obj):
        posts = Post.objects.live().filter(content_type__model=obj["content_type"]).order_by("-date")
        if obj["program"] is not None:
            if obj["program"] not in acceptable_programs:
                raise Http404
            return posts.filter(parent_programs__slug=obj["program"])[:10]

        return posts[:10]
