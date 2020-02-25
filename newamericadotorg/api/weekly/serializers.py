from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField


from weekly.models import WeeklyArticle
from newamericadotorg.api.author.serializers import AuthorSerializer
from newamericadotorg.api.helpers import generate_image_url


class WeeklyArticleSerializer(ModelSerializer):
    authors = SerializerMethodField()
    body = SerializerMethodField()
    post = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_lg = SerializerMethodField()
    story_image_sm = SerializerMethodField()

    def get_authors(self, obj):
        authors = [a.author for a in obj.authors.all().order_by('pk')]
        return AuthorSerializer(authors, many=True).data

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'width-800')

    def get_story_image_lg(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-1400x525')

    def get_story_image_sm(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-400x400')

    def get_body(self, obj):
        return loader.get_template('components/post_body.html').render({ 'page': obj })

    def get_post(self, obj):
        return loader.get_template('components/post_main.html').render({ 'page': obj })

    class Meta:
        model = WeeklyArticle
        fields = (
            'id', 'title', 'date', 'authors', 'body', 'story_image', 'slug',
            'story_excerpt', 'story_image_lg', 'story_image_sm', 'url', 'post'
        )
