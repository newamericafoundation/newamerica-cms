from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from weekly.models import WeeklyEdition, WeeklyArticle
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
        return AuthorSerializer(obj.post_author, many=True, context=self.context).data

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

class WeeklyEditionListSerializer(ModelSerializer):
    number = SerializerMethodField()

    class Meta:
        model = WeeklyEdition
        fields = ('id', 'slug', 'number', 'url')

    def get_number(self, obj):
        return obj.title

    def to_representation(self, obj):
        data = super(WeeklyEditionListSerializer, self).to_representation(obj)
        first_child = obj.get_children().first().specific
        if not first_child:
            return data

        data['title'] = first_child.title
        data['story_image'] = generate_image_url(first_child.story_image, 'fill-180x180')
        data['story_excerpt'] = first_child.story_excerpt

        return data


    def get_story_image(self, obj):
        return generate_image_url(obj.story_image, 'fill-180x180')

class WeeklyEditionSerializer(ModelSerializer):
    articles = SerializerMethodField()
    title = SerializerMethodField()
    number = SerializerMethodField()

    def get_articles(self, obj):
        return WeeklyArticleSerializer(obj.get_children().type(WeeklyArticle).specific().all(), many=True).data

    def get_title(self, obj):
        first_child = obj.get_children().first().specific
        if not first_child:
            return obj.title

        return first_child.title

    def get_number(self, obj):
        return obj.title

    class Meta:
        model = WeeklyEdition
        fields = (
        'id', 'title', 'search_description', 'articles', 'slug', 'first_published_at', 'url',
        'number', 'title'
        )
