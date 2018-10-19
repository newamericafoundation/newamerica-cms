from django.utils.text import slugify
from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from newamericadotorg.api.post.serializers import PostSerializer

from report.models import Report
from newamericadotorg.api.helpers import generate_image_rendition, generate_image_url

class ReportDetailSerializer(PostSerializer):
    featured_sections = SerializerMethodField()
    sections = SerializerMethodField()
    body = SerializerMethodField()
    endnotes = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()
    attachments = SerializerMethodField()
    abstract = SerializerMethodField()
    # spelling fix
    acknowledgments = SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'subheading', 'date', 'content_type', 'featured_sections',
            'authors', 'programs', 'subprograms', 'url', 'story_excerpt',
            'story_image', 'topics', 'sections', 'body', 'endnotes', 'story_image_thumbnail',
            'search_description', 'data_project_external_script', 'attachments', 'acknowledgments', 'abstract'
        )

    def get_story_image(self, obj):
        img = generate_image_rendition(obj.story_image, 'fill-1600x775')
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

    def get_abstract(self, obj):
        if obj.abstract == '<p></p>':
            return None;
        return obj.abstract

    def get_acknowledgments(self, obj):
        if obj.acknowledgements == '<p></p>':
            return None;
        return obj.acknowledgements

    def get_endnotes(self, obj):
        if obj.endnotes:
            endnotes = []
            for e in obj.endnotes:
                endnotes.append({
                    'number': e.value['number'],
                    'note': e.value['note'].source
                })
            return endnotes

    def get_attachments(self,obj):
        attchs = []
        if obj.report_pdf:
            try:
                attchs.append({
                    'title': obj.report_pdf.title,
                    'url': obj.report_pdf.file.url,
                    'size': obj.report_pdf.file.size / 1000,
                    'type': obj.report_pdf.file_extension
                })
            except:
                pass

        if obj.attachment:
            for att in obj.attachment:
                try:
                    attchs.append({
                        'title': att.value.title,
                        'url': att.value.file.url,
                        'size': att.value.file.size / 1000,
                        'type': att.value.file_extension
                    })
                except:
                    pass

        return attchs

    def get_featured_sections(self, obj):
        if obj.featured_sections is None:
            return []
        sections = []
        for i,s in enumerate(obj.featured_sections):
            section = {
                'label': s.value['label'],
                'description': s.value['description'],
                'type': s.value['type'],
                'number': i+1,
                'url': s.value['url']
            }
            sections.append(section)

        return sections


    def get_sections(self, obj):
        if obj.sections is None:
            return None
        sections = []
        for i,s in enumerate(obj.sections):
            slug = slugify(s.value['title'])
            section = {
                'title': s.value['title'],
                'hide_title': s.value['hide_title'],
                'number': i+1,
                'slug': slug,
                'body': s.render(),
                'subsections': [],
                'url': obj.url + slug
            }

            for block in s.value['body']:
                if block.block_type == 'heading':
                    sub_slug = slugify(block.value)
                    section['subsections'].append({
                        'title': block.value,
                        'slug': sub_slug,
                        'url': obj.url + slug + '/#' + sub_slug
                    })
            sections.append(section)

        return sections
