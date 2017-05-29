from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.wagtailcore.models import Page, ContentType
from home.models import Post
from programs.models import Program, Subprogram
from person.models import Person
from issue.models import IssueOrTopic

from django.core.urlresolvers import reverse

from helpers import get_program_content_types, generate_image_url, get_subpages

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
            'id', 'first_name', 'last_name', 'position',
            'short_bio', 'profile_image', 'url'
        )

    def get_position(self, obj):
        return obj.position_at_new_america

    def get_profile_image(self, obj):
        if obj.profile_image:
            return generate_image_url(obj.profile_image, 'fill-300x300')

class PostProgramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url'
        )

    def get_name(self, obj):
        return obj.title;

class PostProjectSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'url'
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
