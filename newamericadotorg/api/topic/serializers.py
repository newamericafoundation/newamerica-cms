from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from issue.models import IssueOrTopic
from newamericadotorg.api.program.serializers import ProgramSubprogramSerializer

class TopicDetailSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()
    body = SerializerMethodField()
    depth = SerializerMethodField()

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

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'body', 'program', 'depth'
        )

class TopicSerializer(ModelSerializer):
    subtopics = SerializerMethodField()
    description = SerializerMethodField()
    program = SerializerMethodField()
    body = SerializerMethodField()
    depth = SerializerMethodField()

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

    class Meta:
        model = IssueOrTopic
        fields = (
            'id', 'url', 'title', 'slug', 'subtopics', 'description', 'program', 'body', 'depth'
        )
