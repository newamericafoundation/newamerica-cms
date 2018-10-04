from django.utils.text import slugify
from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from newamericadotorg.api.post.serializers import PostSerializer

from report.models import Report
from newamericadotorg.api.helpers import generate_image_rendition, generate_image_url

class ReportDetailSerializer(PostSerializer):
    sections = SerializerMethodField()
    body = SerializerMethodField()
    endnotes = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()
    report_pdf = SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type',
            'authors', 'programs', 'subprograms', 'url', 'story_excerpt',
            'story_image', 'topics', 'sections', 'body', 'endnotes', 'story_image_thumbnail',
            'report_pdf', 'search_description', 'data_project_external_script'
        )

    def get_report_pdf(self, obj):
        if not obj.report_pdf:
            return None
        try:
            return obj.report_pdf.file.url
        except:
            return None

    def get_story_image(self, obj):
        img = generate_image_rendition(obj.story_image, 'fill-1300x630')
        if not img:
            return None
        return {
            'url': img.url,
            'height': img.height,
            'width': img.width,
            'source': img.image.source
        }

    def get_story_image_thumbnail(self, obj):
        return generate_image_url(obj.story_image, 'fill-30x14')

    def get_body(self, obj):
        if obj.body:
            return loader.get_template('components/post_body.html').render({ 'page': obj })

    def get_endnotes(self, obj):
        if obj.endnotes:
            endnotes = []
            for e in obj.endnotes:
                endnotes.append({
                    'number': e.value['number'],
                    'note': e.value['note'].source
                })
            return endnotes

    def get_sections(self, obj):
        if obj.sections is None:
            return None
        sections = []
        for i,s in enumerate(obj.sections):
            section = {
                'title': s.value['title'],
                'number': i+1,
                'slug': slugify(s.value['title']),
                'body': s.render(),
                'subsections': []
            }
            for block in s.value['body']:
                if block.block_type == 'heading':
                    section['subsections'].append({
                        'title': block.value,
                        'slug': slugify(block.value)
                    })
            sections.append(section)
        if obj.acknowledgements:
            sections.append({
                'title': 'Acknowledgments',
                'number': len(sections)+1,
                'slug': 'acknowledgments',
                'body': obj.acknowledgements,
                'subsections': []
            })
        return sections
