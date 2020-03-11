from rest_framework.serializers import ModelSerializer, SerializerMethodField

from event.models import Event
from newamericadotorg.api.helpers import generate_image_url, get_content_type
from newamericadotorg.api.program.serializers import PostProgramSerializer, PostSubprogramSerializer


class EventSerializer(ModelSerializer):
    story_image = SerializerMethodField()
    programs = SerializerMethodField()
    subprograms = SerializerMethodField()
    content_type = SerializerMethodField()

    STORY_IMAGE_RENDITIONS = {
        'large': 'fill-700x510',
        'small': 'fill-300x230',
    }

    class Meta:
        model = Event
        fields = ('id', 'title', 'slug', 'date', 'end_date', 'start_time', 'end_time',
        'street_address','city', 'state', 'zipcode', 'rsvp_link', 'story_image',
        'programs', 'subprograms', 'url', 'story_excerpt', 'content_type', 'seo_title', 'online_only'
        )

    def get_story_image(self, obj):
        if obj.story_image:
            rendition_name = self.context['request'].query_params.get('story_image_rendition', None)
            rendition_filter_spec = EventSerializer.STORY_IMAGE_RENDITIONS.get(rendition_name, None)
            return generate_image_url(obj.story_image, rendition_filter_spec)

    def get_programs(self, obj):
        return PostProgramSerializer(obj.parent_programs, many=True).data

    def get_subprograms(self, obj):
        return PostSubprogramSerializer(obj.post_subprogram, many=True).data

    def get_content_type(self, obj):
        return get_content_type(obj)
