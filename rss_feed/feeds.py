from datetime import datetime, time

from django.db import models
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed, Atom1Feed
from django.http import Http404
from wagtail.wagtailcore.models import Page

from home.models import Post
from person.models import Person
from programs.models import Program, Subprogram
from event.models import Event

class CustomFeedType(Rss201rev2Feed):
    # change mime type for browser formatting
    content_type = 'application/xml; charset=utf-8'

    def rss_attributes(self):
        attrs = super(CustomFeedType, self).rss_attributes()
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'
        return attrs

    def add_root_elements(self,handler):
        super(CustomFeedType,self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", u'https://na-production.s3.amazonaws.com/images/newamericalogo_1.original.png')
        handler.addQuickElement(u"title", u'New America')
        handler.addQuickElement(u"link", u'http://newamerica.org/')
        handler.endElement(u"image")

    def add_item_elements(self, handler, item):
        super(CustomFeedType, self).add_item_elements(handler, item)
        media_content = {
            'url': item['media_content_url'],
            'media': 'image'
        }

        handler.addQuickElement(u"media:content", '', media_content )
        handler.addQuickElement(u"media:description", item['description'])


class GenericFeed(Feed):
    def __init__(self):
        super(GenericFeed, self).__init__()
        self.feed_type = CustomFeedType
        self.limit = 20
        self.acceptable_content_types = [
            "book","article","blogpost",
            "event","podcast","policypaper","pressrelease",
            "weeklyarticle","indepthsection",
        ]

        programs = Program.objects.live()
        self.acceptable_programs = [p.slug for p in programs]


    def item_extra_kwargs(self, item):
        extra = super(GenericFeed, self).item_extra_kwargs(item)
        extra.update({'media_content_url': self.item_media_content_url(item) })
        return extra


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
        return Post.objects.live().order_by("-date")[:self.limit]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.story_excerpt

    def item_pubdate(self, item):
         return datetime.combine(item.date, time())

    def item_link(self, item):
        return item.full_url

    def item_media_content_url(self, item):
        if item.story_image is not None:
            return settings.MEDIA_URL + item.story_image.file.url
        return ''


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
        return Post.objects.live().filter(parent_programs__slug=obj["program"]).order_by("-date")[:self.limit]

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
        return Post.objects.live().filter(post_subprogram__slug=obj["subprogram"]).order_by("-date")[:self.limit]

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
        return Post.objects.live().filter(post_author__slug=obj["author"]).order_by("-date")[:self.limit]


class ContentFeed(GenericFeed):
    def get_object(self, request, content_type, program=None):
        if content_type not in self.acceptable_content_types:
            raise Http404

        return {
            "content_type": content_type,
            "program": program,
            "page": Page.objects.live().filter(content_type__model=content_type_model(content_type)).first()
        }

    def items(self, obj):
        posts = Post.objects.live().filter(content_type__model=obj["content_type"]).order_by('-date')

        if obj["program"] is not None:
            if obj["program"] not in self.acceptable_programs:
                raise Http404
            return posts.filter(parent_programs__slug=obj["program"])[:self.limit]

        return posts[:self.limit]

class EventFeed(GenericFeed):
    def get_object(self, request, tense=None):
        return {
            "tense": tense,
            "page": Page.objects.live().filter(content_type__model='alleventshomepage').first()
        }

    def items(self,obj):
        posts = Event.objects.live()
        if obj['tense']:
            today = datetime.now().date()
            if obj['tense'] == 'future':
                posts.filter(date__gte=today).order_by("date","start_time")
            elif obj['tense'] == 'past':
                posts.filter(date__lt=today).order_by("-date","-start_time")
            else:
                 posts.order_by("-date","-start_time")
        else:
            posts.order_by("-date","-state_time")
        return posts[:self.limit]

class EventProgramFeed(GenericFeed):
    def get_object(self, request, program=None, tense=None):
        return {
            "tense": tense,
            "program": program,
            "page": Page.objects.live().filter(content_type__model='alleventshomepage').first()
        }

    def items(self,obj):
        posts = Event.objects.live()
        if obj['tense']:
            today = datetime.now().date()
            if obj['tense'] == 'future':
                posts.filter(date__gte=today).order_by("date", "start_time")
            elif obj['tense'] == 'past':
                posts.filter(date__lt=today).order_by("-date","-start_time")
            else:
                 posts.order_by("-date","-start_time")
        else:
             posts.order_by("-date","-state_time")

        if obj["program"] is not None:
            if obj["program"] not in self.acceptable_programs:
                raise Http404
            return posts.filter(parent_programs__slug=obj["program"])[:self.limit]

        return posts[:self.limit]


def content_type_model(content_type):
    # page exceptions for indepth and weekly content types
    if content_type == "indepthsection":
        content_type_model = "allindepthhomepage"
    elif content_type == "weeklyarticle":
        content_type_model = "weekly"
    else:
        content_type_model = "all"+content_type+"shomepage"

    return content_type_model
