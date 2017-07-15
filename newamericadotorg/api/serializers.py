from django.shortcuts import render
from django.template import loader
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.wagtailcore.models import Page, ContentType
from home.models import Post
from programs.models import Program, Subprogram
from person.models import Person
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyEdition, WeeklyArticle
from in_depth.models import InDepthProject, InDepthSection

from django.core.urlresolvers import reverse

from helpers import get_program_content_types, generate_image_url, get_subpages, get_content_type

class ProgramProjectSerializer(ModelSerializer):
    '''
    Nested under program serializer
    '''
    name = SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'name', 'url', 'title'
        )

    def get_name(self, obj):
        return obj.title


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
    description = SerializerMethodField()
    projects = SerializerMethodField()
    logo = SerializerMethodField()
    content_types = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'description', 'url', 'projects', 'slug',
            'content_types', 'leads', 'features', 'subpages', 'logo'
        )


    def get_description(self, obj):
        return obj.story_excerpt

    def get_projects(self, obj):
        #horribly inefficient. may have to add a ManyToManyField to Program??
        return ProgramProjectSerializer(obj.get_children().type(Subprogram).live(),many=True).data

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


class ProjectProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url'
        )

class ProjectSerializer(ModelSerializer):
    parent_programs = SerializerMethodField()
    content_types = SerializerMethodField()
    description = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'parent_programs', 'url', 'content_types',
             'description', 'leads', 'features', 'subpages'
        )

    def get_parent_programs(self, obj):
        return ProjectProgramSerializer(obj.parent_programs, many=True).data

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
            'short_bio', 'profile_image', 'url', 'leadership'
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

class PostProjectSerializer(ModelSerializer):
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
    projects = SerializerMethodField()
    authors = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'authors', 'programs', 'projects', 'url', 'story_excerpt',
            'story_image'
        )

    def get_content_type(self, obj):
        return {
            'name': obj.content_type.name.title(),
            'api_name': obj.content_type.model
            }

    def get_story_image(self, obj):
        rendition = self.context['request'].query_params.get('image_rendition', None)
        if obj.story_image:
            return generate_image_url(obj.story_image, rendition)

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_projects(self, obj):
        return PostProjectSerializer(obj.post_subprogram, many=True).data

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

class EventSerializer(ModelSerializer):
    story_image = SerializerMethodField()
    programs = SerializerMethodField()
    projects = SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'slug', 'date', 'end_date', 'start_time', 'end_time',
        'street_address','city', 'state', 'zipcode', 'rsvp_link', 'story_image',
        'programs', 'projects', 'url'
        )

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-300x435')

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_projects(self, obj):
        return PostProjectSerializer(obj.post_subprogram, many=True).data

class TopicSerializer(ModelSerializer):

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'title'
        )

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
            return generate_image_url(obj.story_image, 'max-2560x1080')

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
    story_image_sm = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image)
    class Meta:
        model = InDepthProject
        fields = ('id', 'title', 'slug', 'url', 'story_image', 'story_excerpt')

class InDepthProjectSerializer(ModelSerializer):
    sections = SerializerMethodField()
    body = SerializerMethodField()
    story_image = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image)

    def get_body(self, obj):
        if obj.body:
            return loader.get_template('components/in_depth_project_body.html').render({ 'page': obj })

    def get_sections(self, obj):
        return InDepthSectionSerializer(obj.get_children().type(InDepthSection).live().specific(), many=True).data

    class Meta:
        model = InDepthProject
        fields = ('id', 'title', 'slug', 'url', 'story_image', 'search_description', 'body', 'sections', 'data_project_external_script')
