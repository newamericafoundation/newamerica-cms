from django.shortcuts import render
from django.template import loader
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.wagtailcore.models import Page, ContentType
from home.models import Post
from programs.models import Program, Subprogram, AbstractContentPage
from person.models import Person
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyEdition, WeeklyArticle
from in_depth.models import InDepthProject, InDepthSection
from report.models import Report

from django.core.urlresolvers import reverse
from django.utils.text import slugify

from helpers import get_program_content_types, generate_image_url, get_subpages, get_content_type


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


class ProgramSerializer(ModelSerializer):
    description = SerializerMethodField()
    logo = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'title', 'description', 'url', 'logo', 'slug'
        )

    def get_description(self, obj):
        return obj.story_excerpt

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo

class ProgramDetailSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    description = SerializerMethodField()
    subprograms = SerializerMethodField()
    logo = SerializerMethodField()
    content_types = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()
    topics = SerializerMethodField()
    about = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'story_grid', 'description', 'url', 'subprograms', 'slug',
            'content_types', 'leads', 'features', 'subpages', 'logo', 'topics', 'about'
        )

    def get_story_grid(self, obj):
        return loader.get_template('components/story_grid.html').render({ 'page': obj })

    def get_description(self, obj):
        return obj.story_excerpt

    def get_subprograms(self, obj):
        #horribly inefficient. may have to add a ManyToManyField to Program??
        return ProgramSubprogramSerializer(obj.get_children().type(Subprogram).live(),many=True).data

    def get_topics(self, obj):
        return TopicSerializer(obj.get_descendants().filter(content_type__model='issueortopic', depth=5).specific().live(), many=True).data

    def get_content_types(self, obj):
        return get_program_content_types(obj.id)

    def get_leads(self, obj):
        leads = []
        for i in range(4):
            l = 'lead_' + str(i+1)
            if getattr(obj,l,None):
                leads.append(getattr(obj,l).id)
        return leads

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
        return loader.get_template('components/post_body.html').render({ 'page': obj.about_us_page.specific })


class SubprogramProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug'
        )

class SubprogramSerializer(ModelSerializer):
    parent_programs = SerializerMethodField()
    content_types = SerializerMethodField()
    description = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'parent_programs', 'url', 'slug', 'content_types',
             'description', 'leads', 'features', 'subpages'
        )

    def get_parent_programs(self, obj):
        return SubProgramProgramSerializer(obj.parent_programs, many=True).data

    def get_content_types(self, obj):
        return get_program_content_types(obj)

    def get_description(self, obj):
        return obj.story_excerpt

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
        'programs', 'subprograms', 'url'
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

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'authors', 'programs', 'subprograms', 'url', 'story_excerpt',
            'story_image', 'topics', 'sections', 'body', 'endnotes'
        )

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
