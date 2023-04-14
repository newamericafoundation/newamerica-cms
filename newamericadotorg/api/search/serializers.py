from rest_framework.serializers import ModelSerializer, SerializerMethodField

from wagtail.models import Page
from wagtail.images.views.serve import generate_image_url

from person.models import Person
from home.models import Post, Program
from event.models import Event

from newamericadotorg.api.helpers import get_content_type
from newamericadotorg.api.program.serializers import PostProgramSerializer
from newamericadotorg.api.author.serializers import AuthorSerializer

class SearchSerializer(ModelSerializer):

    def to_representation(self, obj):
        data = super(SearchSerializer, self).to_representation(obj)
        obj = obj.specific

        if type(obj) == Person:
            data['profile_image'] = generate_image_url(obj.specific.profile_image, 'fill-300x300') if obj.specific.profile_image else None
            data['first_name'] = obj.first_name
            data['last_name'] = obj.last_name
            data['position'] = obj.position_at_new_america
        elif isinstance(obj, Post) or type(obj) == Event:
            data['date'] = obj.date

        if isinstance(obj, Post):
            data['authors'] = AuthorSerializer(obj.post_author, many=True, context=self.context).data
        
        data['story_image'] = generate_image_url(obj.story_image, 'max-300x240') if getattr(obj, 'story_image', None) else None

        if hasattr(obj, 'parent_programs'):
            data['programs'] = PostProgramSerializer(obj.parent_programs, many=True).data
        else:
            programs = Program.objects.ancestor_of(obj).order_by('-depth')
            data['programs'] = PostProgramSerializer(programs, many=True).data

        data['content_type'] = get_content_type(obj)
        return data

    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'url', 'search_description')
