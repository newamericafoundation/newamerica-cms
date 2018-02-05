from django.shortcuts import render
from django.template import loader
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.wagtailcore.models import Page, ContentType
from home.models import Post, CustomImage
from programs.models import Program, Subprogram, AbstractContentPage
from person.models import Person
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyEdition, WeeklyArticle
from in_depth.models import InDepthProject, InDepthSection
from report.models import Report
from subscribe.models import SubscriptionSegment

from django.core.urlresolvers import reverse
from django.utils.text import slugify

from helpers import get_program_content_types, generate_image_url, generate_image_rendition, get_subpages, get_content_type


class ProgramSubprogramSerializer(ModelSerializer):
    '''
    Nested under program serializer
    '''
    name = SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'name', 'url', 'title', 'slug'
        )
    def get_name(self, obj):
        return obj.title

class TopicDetailSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()
    body = SerializerMethodField()

    def get_subtopics(self, obj):
        return TopicDetailSerializer(obj.get_children().live().specific(), many=True).data

    def get_description(self, obj):
        return obj.story_excerpt

    def get_program(self, obj):
        if obj.parent_program:
            return ProgramSubprogramSerializer(obj.parent_program).data

    def get_body(self, obj):
        if not obj.body:
            return None
        return loader.get_template('components/post_body.html').render({ 'page': obj })

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'body', 'program'
        )

class TopicSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()

    def get_subtopics(self, obj):
        return TopicSerializer(obj.get_children().live().specific(), many=True).data

    def get_description(self, obj):
        return obj.story_excerpt

    def get_program(self, obj):
        if obj.parent_program:
            return ProgramSubprogramSerializer(obj.parent_program).data

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'program'
        )


class SubscriptionSegmentSerializer(ModelSerializer):

    class Meta:
        model = SubscriptionSegment
        fields = (
            'id', 'title', 'ListID', 'SegmentID'
        )


class ProgramSerializer(ModelSerializer):
    logo = SerializerMethodField()
    subprograms = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'title', 'description', 'url', 'logo', 'slug', 'subprograms', 'subscriptions'
        )

    def get_subscriptions(self, obj):
        segments = []
        for s in obj.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_title != '':
                seg['alternate_title'] = s.alternate_title
            segments.append(seg)

        if len(segments) == 0:
            return None
        return segments

    def get_subprograms(self, obj):
        if type(obj) is not Program:
            return None
        #horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(obj.get_children().type(Subprogram).live().in_menu(),many=True).data
        if len(subprograms)==0:
            return None
        return subprograms

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo

class StoryGridItemSerializer(ModelSerializer):
    content_type = SerializerMethodField()
    story_image = SerializerMethodField()
    story_excerpt = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()

    def get_story_excerpt(self, obj):
        return obj.specific.story_excerpt

    def get_story_image(self, obj):
        if 'is_lead' in self.context:
            return generate_image_url(obj.specific.story_image, 'fill-800x375')
        return generate_image_url(obj.specific.story_image, 'fill-600x460')

    def get_story_image_thumbnail(self, obj):
        if 'is_lead' in self.context:
            return generate_image_url(obj.specific.story_image, 'fill-32x15')
        return generate_image_url(obj.specific.story_image, 'fill-30x23')

    def get_content_type(self, obj):
        content_type = obj.get_ancestors().type(AbstractContentPage).first()
        if content_type:
            return {
                'id': content_type.id,
                'name': content_type.title,
                'title': obj.content_type.name.title(),
                'api_name': obj.content_type.model,
                'url': content_type.url,
                'slug': content_type.slug
                }
        return get_content_type(obj.content_type.model)

    class Meta:
        model = Page
        fields = ('id', 'title', 'url', 'slug', 'content_type', 'story_image', 'story_excerpt', 'story_image_thumbnail')

class ProgramDetailSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    description = SerializerMethodField()
    subprograms = SerializerMethodField()
    logo = SerializerMethodField()
    content_types = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()
    topics = SerializerMethodField()
    about = SerializerMethodField()
    about_us_pages = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'story_grid', 'description', 'url', 'subprograms', 'slug',
            'content_types', 'features', 'subpages', 'logo', 'topics', 'about', 'about_us_pages',
            'subscriptions'
        )

    def get_story_grid(self, obj):
        grid = []
        if obj.lead_1:
            context = self.context.copy()
            context['is_lead'] = True
            grid.append(StoryGridItemSerializer(obj.lead_1.specific, context=context).data)
        if obj.lead_2:
            grid.append(StoryGridItemSerializer(obj.lead_2.specific, context=self.context).data)
        if obj.lead_3:
            grid.append(StoryGridItemSerializer(obj.lead_3.specific, context=self.context).data)
        if obj.lead_4:
            grid.append(StoryGridItemSerializer(obj.lead_4.specific, context=self.context).data)
        if obj.feature_1:
            grid.append(StoryGridItemSerializer(obj.feature_1.specific, context=self.context).data)
        if obj.feature_2:
            grid.append(StoryGridItemSerializer(obj.feature_2.specific, context=self.context).data)
        if obj.feature_3:
            grid.append(StoryGridItemSerializer(obj.feature_3.specific, context=self.context).data)

        return grid

    def get_description(self, obj):
        return obj.description or obj.story_excerpt

    def get_subprograms(self, obj):
        #horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(obj.get_children().type(Subprogram).live().in_menu(),many=True).data
        if len(subprograms)==0:
            return None
        return subprograms

    def get_topics(self, obj):
        topics = TopicDetailSerializer(obj.get_descendants().filter(content_type__model='issueortopic', depth=5).specific().live(), many=True).data
        if len(topics)==0:
            return None
        return topics

    def get_content_types(self, obj):
        return get_program_content_types(obj.id)

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo

    def get_features(self, obj):
        features = []
        for i in range(3):
            f = 'features_' + str(i+1)
            if getattr(obj,f,None):
                features.append(getattr(obj,f).id)
        return features

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        if not obj.about_us_page:
            return None;
        return loader.get_template('components/post_body.html').render({ 'page': obj.about_us_page.specific })

    def get_about_us_pages(self, obj):
        if not obj.sidebar_menu_about_us_pages:
            return None
        if len(obj.sidebar_menu_about_us_pages) == 0:
            return None

        about_us_pages = []
        for p in obj.sidebar_menu_about_us_pages:
            p = p.value.specific
            if p.title == 'About Us' or p.title == 'Our People':
                continue
            body = loader.get_template('components/post_body.html').render({ 'page': p })
            about_us_pages.append({ 'title': p.title, 'body': body, 'slug': p.slug })

        if len(about_us_pages) == 0:
            return None

        return about_us_pages

    def get_subscriptions(self, obj):
        segments = []
        for s in obj.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_title != '':
                seg['alternate_title'] = s.alternate_title
            segments.append(seg)

        if len(segments) == 0:
            return None
        return segments


class SubprogramProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug'
        )

class SubprogramSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    parent_programs = SerializerMethodField()
    content_types = SerializerMethodField()
    description = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()
    about = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'story_grid', 'parent_programs', 'url', 'slug', 'content_types',
             'description', 'leads', 'features', 'subpages', 'about'
        )

    def get_parent_programs(self, obj):
        parents = SubprogramProgramSerializer(obj.parent_programs, many=True).data
        if len(parents)==0:
            return None
        return parents

    def get_story_grid(self, obj):
        grid = []
        context = self.context
        if obj.template == 'simple_program.html':
            context['is_lead'] = True
        if obj.lead_1:
            lead_context = self.context.copy()
            lead_context['is_lead'] = True
            grid.append(StoryGridItemSerializer(obj.lead_1.specific, context=lead_context).data)
        if obj.lead_2:
            grid.append(StoryGridItemSerializer(obj.lead_2.specific, context=context).data)
        if obj.lead_3:
            grid.append(StoryGridItemSerializer(obj.lead_3.specific, context=context).data)
        if obj.lead_4:
            grid.append(StoryGridItemSerializer(obj.lead_4.specific, context=context).data)
        if obj.feature_1:
            grid.append(StoryGridItemSerializer(obj.feature_1.specific, context=context).data)
        if obj.feature_2:
            grid.append(StoryGridItemSerializer(obj.feature_2.specific, context=context).data)
        if obj.feature_3:
            grid.append(StoryGridItemSerializer(obj.feature_3.specific, context=context).data)

        return grid

    def get_content_types(self, obj):
        return get_program_content_types(obj)

    def get_description(self, obj):
        return obj.description or obj.story_excerpt

    def get_leads(self, obj):
        leads = []
        for i in range(4):
            l = 'lead_' + str(i+1)
            if getattr(obj,l,None):
                leads.append(getattr(obj,l).id)
        return leads

    def get_features(self, obj):
        features = []
        for i in range(3):
            f = 'features_' + str(i+1)
            if getattr(obj,f,None):
                features.append(getattr(obj,f).id)
        return features

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        if not obj.about_us_page:
            return None;
        return loader.get_template('components/post_body.html').render({ 'page': obj.about_us_page.specific })


class AuthorSerializer(ModelSerializer):
    position = SerializerMethodField()
    profile_image = SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'id', 'first_name', 'last_name', 'position', 'role',
            'short_bio', 'profile_image', 'url', 'leadership', 'topics'
        )

    def get_position(self, obj):
        return obj.position_at_new_america

    def get_profile_image(self, obj):
        if obj.profile_image:
            return generate_image_url(obj.profile_image, 'fill-200x200')

class PostProgramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug'
        )

    def get_name(self, obj):
        return obj.title;

class PostSubprogramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'url', 'slug'
        )

    def get_name(self, obj):
        return obj.title;

class PostSerializer(ModelSerializer):
    content_type = SerializerMethodField()
    story_image = SerializerMethodField()
    programs = SerializerMethodField()
    subprograms = SerializerMethodField()
    authors = SerializerMethodField()
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'authors', 'programs', 'subprograms', 'url', 'story_excerpt',
            'story_image', 'topics'
        )

    def get_content_type(self, obj):
        content_type = obj.get_ancestors().type(AbstractContentPage).first()
        return {
            'id': content_type.id,
            'name': content_type.title,
            'title': obj.content_type.name.title(),
            'api_name': obj.content_type.model,
            'url': content_type.url,
            'slug': content_type.slug
            }

    def get_story_image(self, obj):
        rendition = self.context['request'].query_params.get('image_rendition', None)
        if obj.story_image:
            return generate_image_url(obj.story_image, rendition)

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_subprograms(self, obj):
        return PostSubprogramSerializer(obj.post_subprogram, many=True).data

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

class EventSerializer(ModelSerializer):
    story_image = SerializerMethodField()
    programs = SerializerMethodField()
    subprograms = SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'slug', 'date', 'end_date', 'start_time', 'end_time',
        'street_address','city', 'state', 'zipcode', 'rsvp_link', 'story_image',
        'programs', 'subprograms', 'url', 'story_excerpt'
        )

    def get_story_image(self, obj):
        if obj.story_image:
            rendition = self.context['request'].query_params.get('image_rendition', None)
            return generate_image_url(obj.story_image, rendition)

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_subprograms(self, obj):
        return PostSubprogramSerializer(obj.post_subprogram, many=True).data

class HomeSerializer(ModelSerializer):
    leads = SerializerMethodField()
    features = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'leads', 'features'
        )

    def get_leads(self, obj):
        leads = []
        for i in range(4):
            l = 'lead_' + str(i+1)
            if getattr(obj,l,None):
                leads.append(getattr(obj,l).id)
        return leads

    def get_features(self, obj):
        features = []
        for i in range(3):
            f = 'features_' + str(i+1)
            if getattr(obj,f,None):
                features.append(getattr(obj,f).id)
        return features

class WeeklyEditionArticleSerializer(ModelSerializer):
    authors = SerializerMethodField()
    story_image = SerializerMethodField()

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

    def get_story_image(self, obj):
        if(obj.story_image):
            return generate_image_url(obj.story_image, 'fill-300x300')

    class Meta:
        model = WeeklyArticle
        fields = (
            'id', 'title', 'search_description', 'authors', 'slug', 'story_image'
        )

class WeeklyArticleSerializer(ModelSerializer):
    authors = SerializerMethodField()
    body = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_md = SerializerMethodField()
    story_image_sm = SerializerMethodField()

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'max-1200x600')

    def get_story_image_md(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-600x600')

    def get_story_image_sm(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-300x300')

    def get_body(self, obj):
        return loader.get_template('components/post_body.html').render({ 'page': obj })

    class Meta:
        model = WeeklyArticle
        fields = (
            'id', 'title', 'date', 'authors', 'body', 'story_image', 'slug',
            'story_excerpt', 'story_image_md', 'story_image_sm'
        )

class WeeklyEditionListSerializer(ModelSerializer):
    class Meta:
        model = WeeklyEdition
        fields = ('id', 'title', 'slug')

class WeeklyEditionSerializer(ModelSerializer):
    articles = SerializerMethodField()

    def get_articles(self, obj):
        return WeeklyArticleSerializer(obj.get_children().type(WeeklyArticle).specific().live(), many=True).data

    class Meta:
        model = WeeklyEdition
        fields = (
        'id', 'title', 'search_description', 'articles', 'slug', 'first_published_at'
        )

class SearchSerializer(ModelSerializer):
    specific = SerializerMethodField()

    def get_specific(self, obj):
        spec = {
            'id': obj.id,
            'title': obj.title,
            'slug': obj.slug,
            'url': obj.url,
            'image': None,
            'date': None,
            'content_type': get_content_type(obj.content_type.model),
            'authors': [],
            'description': None,
            'programs': []
        }
        if not self.context['request'].query_params.get('exclude_images', None)=='true':
            if getattr(obj.specific, 'story_image', None):
                spec['image'] = generate_image_url(obj.specific.story_image, 'min-650x200')
            if getattr(obj.specific, 'profile_image', None):
                spec['image'] = generate_image_url(obj.specific.profile_image, 'fill-300x300')
        if getattr(obj.specific, 'date', None):
            spec['date'] = obj.specific.date
        if getattr(obj.specific, 'post_author', None):
            spec['authors'] = AuthorSerializer(obj.specific.post_author, many=True, context=self.context).data
        if getattr(obj.specific, 'story_excerpt', None):
            spec['description'] = obj.specific.story_excerpt
        if getattr(obj.specific, 'short_bio', None):
            spec['description'] = obj.specific.short_bio
        if getattr(obj.specific, 'parent_programs', None):
            spec['programs'] = PostProgramSerializer(obj.specific.parent_programs, many=True).data
        if getattr(obj.specific, 'belongs_to_these_programs', None):
            spec['programs'] = PostProgramSerializer(obj.specific.belongs_to_these_programs, many=True).data
        if obj.content_type.model == 'person':
            spec['content_type']['name'] = obj.specific.role

        return spec

    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'url', 'search_description', 'specific')

class InDepthSectionSerializer(ModelSerializer):
    body = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_sm = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'max-1920x1080')

    def get_story_image_sm(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-150x150')


    def get_body(self, obj):
        return loader.get_template('components/in_depth_body.html').render({ 'page': obj })

    class Meta:
        model = InDepthSection
        fields = ('id', 'title', 'subheading', 'slug', 'url', 'story_excerpt', 'story_image', 'story_image_sm', 'body')

class InDepthProjectListSerializer(ModelSerializer):
    story_image = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'max-1920x1080')
    class Meta:
        model = InDepthProject
        fields = ('id', 'title', 'slug', 'url', 'story_image', 'story_excerpt')

class InDepthProjectSerializer(ModelSerializer):
    sections = SerializerMethodField()
    body = SerializerMethodField()
    story_image = SerializerMethodField()
    buttons = SerializerMethodField()
    authors = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'max-1920x1080')

    def get_body(self, obj):
        if obj.body:
            return loader.get_template('components/in_depth_project_body.html').render({ 'page': obj })

    def get_sections(self, obj):
        return InDepthSectionSerializer(obj.get_children().type(InDepthSection).live().specific(), many=True).data

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

    def get_buttons(self, obj):
        buttons = []
        if obj.buttons:
            for b in obj.buttons:
                buttons.append({ 'text': b.value['button_text'], 'url': b.value['button_url']})
        return buttons
    class Meta:
        model = InDepthProject
        fields = (
        'id', 'title', 'slug', 'url', 'story_image', 'authors',
        'search_description', 'body', 'sections', 'buttons',
        'data_project_external_script', 'subheading')

class ReportDetailSerializer(PostSerializer):
    sections = SerializerMethodField()
    body = SerializerMethodField()
    endnotes = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'authors', 'programs', 'subprograms', 'url', 'story_excerpt',
            'story_image', 'topics', 'sections', 'body', 'endnotes', 'story_image_thumbnail'
        )

    def get_story_image(self, obj):
        img = generate_image_rendition(obj.story_image, 'fill-1100x495')
        if not img:
            return None
        return {
            'url': img.url,
            'height': img.height,
            'width': img.width,
            'source': img.image.source
        }

    def get_story_image_thumbnail(self, obj):
        return generate_image_url(obj.story_image, 'fill-30x14')

    def get_body(self, obj):
        if obj.body:
            return loader.get_template('components/post_body.html').render({ 'page': obj })

    def get_endnotes(self, obj):
        if obj.endnotes:
            endnotes = []
            for e in obj.endnotes:
                endnotes.append({
                    'number': e.value['number'],
                    'note': e.value['note'].source
                })
            return endnotes

    def get_sections(self, obj):
        if obj.sections is None:
            return None
        sections = []
        for i,s in enumerate(obj.sections):
            section = {
                'title': s.value['title'],
                'number': i+1,
                'slug': slugify(s.value['title']),
                'body': s.render(),
                'subsections': []
            }
            for block in s.value['body']:
                if block.block_type == 'heading':
                    section['subsections'].append({
                        'title': block.value,
                        'slug': slugify(block.value)
                    })
            sections.append(section)
        return sections


class HomeDetailSerializer(PostSerializer):
    data = SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'slug', 'url', 'story_excerpt',
            'data'
        )

    def get_data(self, obj):
        panels = None
        for d in obj.body.stream_data:
            # only the first panels is relevant
            if d['type'] == 'panels':
                panels = d['value']
                break
        if not panels:
            return None

        data = {}

        for p in panels:
            d = {}
            panel_key = p['value']['title']
            for b in p['value']['body']:
                key = b['type']

                if not key in d:
                    d[key] = []

                if key == 'inline_image':
                    img = CustomImage.objects.get(pk=b['value']['image'])
                    b['value']['url'] = generate_image_url(img, 'width-1100')
                d[key].append(b['value'])

            data[panel_key] = d

        return data
