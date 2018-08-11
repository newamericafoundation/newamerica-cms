from rest_framework.serializers import ModelSerializer, SerializerMethodField

from home.models import Post
from newamericadotorg.api.helpers import generate_image_url, get_content_type
from newamericadotorg.api.author.serializers import AuthorSerializer
from newamericadotorg.api.program.serializers import PostProgramSerializer, PostSubprogramSerializer

class PostSimpleSerializer(ModelSerializer):
    content_type = SerializerMethodField()
    story_image = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'url', 'story_excerpt', 'story_image', 'topics', 'seo_title'
        )

    def get_content_type(self, obj):
        return get_content_type(obj)

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-675x250')

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
            'story_image', 'topics', 'seo_title'
        )

    def get_content_type(self, obj):
        return get_content_type(obj)

    def get_story_image(self, obj):
        rendition = self.context['request'].query_params.get('image_rendition', None)
        if obj.story_image:
            return generate_image_url(obj.story_image, rendition)

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_subprograms(self, obj):
        return PostSubprogramSerializer(obj.post_subprogram, many=True).data

    def get_authors(self, obj):
        authors_rel = obj.authors.order_by('pk')
        if authors_rel is None:
            return None
        authors = [rel.author for rel in authors_rel]
        return AuthorSerializer(authors, many=True, context=self.context).data
