from rest_framework.serializers import ModelSerializer, SerializerMethodField

from home.models import CustomImage, OrgSimplePage
from programs.models import Program
from report.models import Report
from newamericadotorg.api.post.serializers import PostSerializer
from newamericadotorg.api.helpers import generate_image_url
# from wagtail.documents.models import Document

class HomeDetailSerializer(PostSerializer):
    data = SerializerMethodField()
    subpages = SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'slug', 'url', 'story_excerpt',
            'data', 'subpages', 'data_project_external_script'
        )

    def get_subpages(self, obj):

        subpages = OrgSimplePage.objects.child_of(obj).filter(custom_interface=True).live()

        return HomeDetailSerializer(subpages, many=True).data

    def get_data(self, obj):
        panels = None
        for d in obj.body.stream_data:
            # only the first panels is relevant
            if d['type'] == 'panels':
                panels = d['value']
                break
        if not panels:
            return None

        data = {}

        for p in panels:
            d = {}
            panel_key = p['value']['title']
            for b in p['value']['body']:
                key = b['type']

                if not key in d:
                    d[key] = []

                if key == 'inline_image':
                    img = CustomImage.objects.get(pk=b['value']['image'])
                    b['value']['url'] = generate_image_url(img, 'fill-800x550')
                elif key == 'resource_kit':
                    for r in b['value']['resources']:
                        id = r['value']['resource']
                        if r['type'] == 'attachment':
                            resource = Document.objects.get(pk=id)
                            r['value']['resource'] = resource.url
                        elif r['type'] == 'post':
                            resource = Page.objects.get(pk=id)
                            r['value']['resource'] = resource.url
                d[key].append(b['value'])

            data[panel_key] = d

        return data
