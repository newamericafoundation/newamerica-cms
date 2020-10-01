import datetime

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from wagtail.images.views.serve import generate_image_url

from person.models import Person, PersonProgramRelationship, PersonSubprogramRelationship

class AuthorSerializer(ModelSerializer):
    position = SerializerMethodField()
    profile_image = SerializerMethodField()
    full_name = SerializerMethodField()
    group = SerializerMethodField()

    class Meta:
        model = Person
        fields = (
            'id', 'first_name', 'last_name', 'position', 'role',
            'short_bio', 'profile_image', 'url', 'leadership',
            'full_name', 'former', 'expertise', 'group'
        )

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name;

    def get_position(self, obj):
        return obj.position_at_new_america

    def get_profile_image(self, obj):
        if obj.profile_image:
            return generate_image_url(obj.profile_image, 'fill-200x200')

    def get_group(self,obj):
        program_id = self.context.get('program_id', None)
        subprogram_id = self.context.get('subprogram_id')
        rel = None

        if program_id:
            rel = PersonProgramRelationship.objects.filter(program__id=program_id, person=obj).first()
        elif subprogram_id:
            rel = PersonSubprogramRelationship.objects.filter(subprogram__id=subprogram_id, person=obj).first()
        else:
            return None

        if not rel: return 'Staff'

        this_year = datetime.datetime.now().year

        if rel.group == 'Current Fellows':
            if rel.fellowship_year and rel.fellowhip_year != this_year:
                return 'Returning Fellows'
            return rel.group
        elif rel.group == 'Former Fellows':
            if rel.fellowship_year:
                return str(rel.fellowship_year) + ' Fellows'
            return rel.group
        elif obj.role == 'Fellow':
            if obj.former:
                if obj.fellowship_year:
                    return str(obj.fellowship_year) + ' Fellows'
                return 'Former Fellows'
            else:
                if obj.fellowship_year and obj.fellowship_year != this_year:
                    return 'Returning Fellows'
                return 'Current Fellows'
        if rel.group is None: return 'Staff'

        return rel.group
