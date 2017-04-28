from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.wagtailcore.models import Page, ContentType
from home.models import Post
from programs.models import Program, Subprogram
from person.models import Person

from django.core.urlresolvers import reverse
from wagtail.wagtailimages.utils import generate_signature

from helpers import get_content_types

class ProgramSubprogramSerializer(ModelSerializer):
    name = SerializerMethodField()
    content_types = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'name', 'url', 'slug', 'content_types', 'leads', 'features'
        )

    def get_name(self, obj):
        return obj.title

    def get_content_types(self, obj):
        return get_content_types(obj)

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

class ProgramSerializer(ModelSerializer):
    logo = SerializerMethodField()
    description = SerializerMethodField()
    subprograms = SerializerMethodField()
    content_types = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'description', 'url', 'subprograms', 'logo', 'slug',
            'content_types', 'leads', 'features'
        )

    def get_logo(self, obj):
        return obj.desktop_program_logo

    def get_description(self, obj):
        return obj.story_excerpt

    def get_subprograms(self, obj):
        #horribly inefficient. may have to add a ManyToManyField to Program??
        return ProgramSubprogramSerializer(obj.get_subprograms(),many=True).data

    def get_content_types(self, obj):
        return get_content_types(obj)

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


class SubprogramProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug'
        )

class SubprogramSerializer(ModelSerializer):
    parent_programs = SerializerMethodField()
    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'parent_programs', 'url', 'slug'
        )

    def get_parent_programs(self, obj):
        return SubprogramProgramSerializer(obj.parent_programs, many=True).data

class AuthorSerializer(ModelSerializer):
    position = SerializerMethodField()
    full_name = SerializerMethodField()
    profile_image = SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'id', 'full_name', 'first_name', 'last_name', 'role', 'position',
            'short_bio', 'long_bio', 'profile_image', 'slug'
        )

    def get_position(self, obj):
        return obj.position_at_new_america

    def get_full_name(self, obj):
        return obj.title

    def get_profile_image(self, obj):
        rendition = self.context['request'].query_params.get('image_rendition', None)
        if obj.profile_image:
            return generate_image_url(obj.profile_image, rendition)

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
            'story_image', 'slug'
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
        return ProgramSerializer(obj.parent_programs, many=True).data

    def get_subprograms(self, obj):
        return SubprogramSerializer(obj.post_subprogram, many=True).data

    def get_authors(self, obj):
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

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


def generate_image_url(image, filter_spec=None):
    if not filter_spec:
        return image.file.url

    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    return url
