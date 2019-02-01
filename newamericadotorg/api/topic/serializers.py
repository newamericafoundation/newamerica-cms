from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issue.models import IssueOrTopic
from newamericadotorg.api.program.serializers import ProgramSubprogramSerializer
from newamericadotorg.api.post.serializers import PostSimpleSerializer

class TopicSingleSerializer(ModelSerializer):
    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug'
        )

class TopicDetailSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()
    body = SerializerMethodField()
    depth = SerializerMethodField()
    featured_publications = SerializerMethodField()

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

    def get_depth(self, obj):
        return obj.depth - 5

    def get_featured_publications(self, obj):
        featured  = []
        if obj.featured_publication_1:
            featured.append(PostSimpleSerializer(obj.featured_publication_1.specific).data)
        if obj.featured_publication_2:
            featured.append(PostSimpleSerializer(obj.featured_publication_2.specific).data)
        if obj.featured_publication_3:
            featured.append(PostSimpleSerializer(obj.featured_publication_3.specific).data)

        return featured

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'body', 'program', 'depth',
            'featured_publications'
        )

class TopicSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()
    body = SerializerMethodField()
    depth = SerializerMethodField()
    featured_publications = SerializerMethodField()

    def get_subtopics(self, obj):
        return TopicSerializer(obj.get_children().live().specific(), many=True).data

    def get_description(self, obj):
        return obj.story_excerpt

    def get_body(self, obj):
        if not obj.body:
            return None
        return loader.get_template('components/post_body.html').render({ 'page': obj })

    def get_program(self, obj):
        if obj.parent_program:
            return obj.parent_program.id

    def get_depth(self, obj):
        return obj.depth - 5

    def get_featured_publications(self, obj):
        featured  = []
        if obj.featured_publication_1:
            featured.append(PostSimpleSerializer(obj.featured_publication_1.specific).data)
        if obj.featured_publication_2:
            featured.append(PostSimpleSerializer(obj.featured_publication_2.specific).data)
        if obj.featured_publication_3:
            featured.append(PostSimpleSerializer(obj.featured_publication_3.specific).data)

        return featured


    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'program', 'body', 'depth',
            'featured_publications'
        )
