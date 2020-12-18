from django.utils.text import slugify
from django.template import loader

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import ListAPIView

from newamericadotorg.api.post.serializers import PostSerializer

from survey.models import Survey, Commentary, Commented_Survey

class SurveyDetailSerializer(ModelSerializer):
    # study_title = SerializerMethodField()
    # # org = SerializerMethodField()
    # # year = SerializerMethodField()
    # month = SerializerMethodField()
    # sample_number = SerializerMethodField()
    # sample_demos = SerializerMethodField()
    # # demos_key = SerializerMethodField()
    # findings = SerializerMethodField()
    # link = SerializerMethodField()
    # # spelling fix
    # file = SerializerMethodField()
    # # assoc_commentary = SerializerMethodField()

    class Meta:
        model = Survey
        fields = ('id', 'title', 'study_title', 'date', 'content_type', 'org',
            'url', 'sample_number', 'findings', 'link', 'file'
        )
    def get_content_type(self, obj):
        return get_content_type(obj)


    # def get_story_image(self, obj):
    #     img = generate_image_rendition(obj.story_image, 'fill-1600x775')
    #     if not img:
    #         return None
    #     return {
    #         'url': img.url,
    #         'height': img.height,
    #         'width': img.width,
    #         'source': img.image.source
    #     }

    # def get_story_image_thumbnail(self, obj):
    #     if obj.story_image:
    #         return generate_image_url(obj.story_image, 'fill-30x14')

    # def get_partner_logo(self, obj):
    #     if obj.partner_logo:
    #         return generate_image_url(obj.partner_logo, 'max-240x30')

    # def get_body(self, obj):
    #     if obj.body:
    #         return loader.get_template('components/post_body.html').render({ 'page': obj })

    def get_findings(self, obj):
        if obj.findings == '<p></p>':
            return None;
        return obj.findings

    def get_study_title(self, obj):
        return obj.study_title

    def get_org(self, obj):
        return obj.org

    def get_year(self, obj):
       return obj.year

    # def get_month(self, obj):
    #    return obj.month

    def get_sample_number(self, obj):
       return obj.sample_number

    # def get_sample_demos(self, obj):
    #    return obj.sample_demos

    # # def get_demos_key(self, obj):
    # #    return obj.demos_key
       
    def get_link(self, obj):
       return obj.link
    
    def get_file(self, obj):
       return obj.file
    

    # def get_attachments(self,obj):
    #     attchs = []
    #     if obj.report_pdf:
    #         try:
    #             attchs.append({
    #                 'title': obj.report_pdf.title,
    #                 'url': obj.report_pdf.file.url,
    #                 'size': obj.report_pdf.file.size / 1000,
    #                 'type': obj.report_pdf.file_extension
    #             })
    #         except:
    #             pass

    #     if obj.attachment:
    #         for att in obj.attachment:
    #             try:
    #                 attchs.append({
    #                     'title': att.value.title,
    #                     'url': att.value.file.url,
    #                     'size': att.value.file.size / 1000,
    #                     'type': att.value.file_extension
    #                 })
    #             except:
    #                 pass

    #     return attchs

    # def get_featured_sections(self, obj):
    #     if obj.featured_sections is None:
    #         return []
    #     sections = []
    #     for i,s in enumerate(obj.featured_sections):
    #         section = {
    #             'label': s.value['label'],
    #             'description': s.value['description'],
    #             'type': s.value['type'],
    #             'number': i+1,
    #             'url': s.value['url']
    #         }
    #         sections.append(section)

    #     return sections


    # def get_sections(self, obj):
    #     if obj.sections is None:
    #         return None
    #     sections = []
    #     for i,s in enumerate(obj.sections):
    #         slug = slugify(s.value['title'])
    #         section = {
    #             'title': s.value['title'],
    #             'hide_title': s.value['hide_title'],
    #             'number': i+1,
    #             'slug': slug,
    #             'body': s.render(),
    #             'subsections': [],
    #             'url': obj.url + slug
    #         }

    #         for block in s.value['body']:
    #             if block.block_type == 'heading':
    #                 sub_slug = slugify(block.value)
    #                 section['subsections'].append({
    #                     'title': block.value,
    #                     'slug': sub_slug,
    #                     'url': obj.url + slug + '/#' + sub_slug
    #                 })
    #         sections.append(section)

    #     return sections

    # def get_topics(self, obj):
    #     if obj.topics is None:
    #         return None
    #     topics = [o.topic for o in obj.topics.all()]
    #     return TopicSingleSerializer(topics, many=True).data