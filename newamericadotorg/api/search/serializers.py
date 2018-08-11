from rest_framework.serializers import ModelSerializer, SerializerMethodField

from wagtail.core.models import Page

from person.models import Person
from home.models import Post
from event.models import Event

from newamericadotorg.api.helpers import generate_image_url, get_content_type
from newamericadotorg.api.program.serializers import PostProgramSerializer
from newamericadotorg.api.author.serializers import AuthorSerializer

class SearchSerializer(ModelSerializer):

    def to_representation(self, obj):
        data = super(SearchSerializer, self).to_representation(obj)
        obj = obj.specific

        if type(obj) == Person:
            data['profile_image'] = generate_image_url(obj.specific.profile_image, 'fill-300x300')
            data['first_name'] = obj.first_name
            data['last_name'] = obj.last_name
            data['position'] = obj.position_at_new_america
        elif isinstance(obj, Post) or type(obj) == Event:
            data['story_image'] = generate_image_url(obj.story_image, 'max-300x240')
            data['date'] = obj.date
            data['programs'] = PostProgramSerializer(obj.parent_programs, many=True).data

        if isinstance(obj, Post):
            data['authors'] = AuthorSerializer(obj.post_author, many=True, context=self.context).data


        data['content_type'] = get_content_type(obj)
        return data

    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'url', 'search_description')
