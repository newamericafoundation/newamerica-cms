from django.template import loader

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    IntegerField,
)

from wagtail.images.views.serve import generate_image_url

from the_thread.models import ThreadArticle, Thread
from newamericadotorg.api.author.serializers import AuthorSerializer


class ThreadSerializer(ModelSerializer):
    featured_pages = SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'title',
            'featured_pages',
        )

    def get_featured_pages(self, obj):
        featured = []
        if obj.featured_page_1:
            featured.append(
                ListingThreadArticleSerializer(
                    obj.featured_page_1.specific
                ).data
            )
        if obj.featured_page_2:
            featured.append(
                ListingThreadArticleSerializer(
                    obj.featured_page_2.specific
                ).data
            )
        if obj.featured_page_3:
            featured.append(
                ListingThreadArticleSerializer(
                    obj.featured_page_3.specific
                ).data
            )
        return featured


class ListingThreadArticleSerializer(ModelSerializer):
    authors = SerializerMethodField()
    story_image_lg = SerializerMethodField()
    story_image_sm = SerializerMethodField()

    def get_authors(self, obj):
        authors = [a.author for a in obj.authors.all()]
        return AuthorSerializer(authors, many=True).data

    def get_story_image_lg(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-1400x525')

    def get_story_image_sm(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'fill-400x400')

    class Meta:
        model = ThreadArticle
        fields = (
            'id', 'title', 'date', 'authors', 'slug',
            'story_excerpt', 'story_image_lg', 'story_image_sm', 'url',
            'story_image_alt',
        )   


class DetailThreadArticleSerializer(ListingThreadArticleSerializer):
    body = SerializerMethodField()
    post = SerializerMethodField()
    story_image = SerializerMethodField()

    def get_story_image(self, obj):
        if obj.story_image:
            return generate_image_url(obj.story_image, 'width-800')

    def get_post(self, obj):
        return loader.get_template('components/post_main.html').render({ 'page': obj })

    def get_body(self, obj):
        return loader.get_template('components/post_body.html').render({ 'page': obj })

    class Meta:
        model = ThreadArticle
        fields = (
            'id', 'title', 'date', 'authors', 'body', 'story_image', 'slug',
            'story_excerpt', 'story_image_lg', 'story_image_sm', 'url', 'post',
            'story_image_alt',
        )
