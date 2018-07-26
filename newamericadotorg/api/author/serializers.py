import datetime

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from person.models import Person
from newamericadotorg.api.helpers import generate_image_url

class AuthorSerializer(ModelSerializer):
    position = SerializerMethodField()
    profile_image = SerializerMethodField()
    fellowship_year = SerializerMethodField()
    full_name = SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'id', 'first_name', 'last_name', 'position', 'role',
            'short_bio', 'profile_image', 'url', 'leadership', 'topics',
            'fellowship_year', 'full_name', 'former'
        )

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name;

    def get_position(self, obj):
        return obj.position_at_new_america

    def get_profile_image(self, obj):
        if obj.profile_image:
            return generate_image_url(obj.profile_image, 'fill-200x200')

    def get_fellowship_year(self, obj):
        if obj.fellowship_year:
            if not obj.former and obj.fellowship_year != datetime.date.today().year:
                return 'Returning'
            return obj.fellowship_year
