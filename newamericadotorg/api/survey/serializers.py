from rest_framework.serializers import ModelSerializer, SerializerMethodField
from survey.models import Survey, SurveysHomePage
from newamericadotorg.api.author.serializers import AuthorSerializer
from wagtail.images.views.serve import generate_image_url


class SurveyHomeSerializer(ModelSerializer):
    surveys = SerializerMethodField()
    page_author = SerializerMethodField()
    partner_logo = SerializerMethodField()
    parent = SerializerMethodField()
    class Meta:
        model = SurveysHomePage
        fields = ['id', 'title', 'url_path', 'parent', 'about', 'methodology', 'subscribe', 'page_author', 'submissions', 'about_submission', 'surveys', 'partner_logo', 'subheading']
        depth = 1
        read_only_fields = fields
    def get_surveys(self, obj):
        return get_surveys_detail(obj)
    
    def get_page_author(self, obj):
        authors_rel = obj.authors.all()
        if not authors_rel:
            return None
        authors = [rel.author for rel in authors_rel]
        return AuthorSerializer(authors, many=True, context=self.context).data
   
    def get_partner_logo(self, obj):
        if obj.partner_logo:
            return generate_image_url(obj.partner_logo, 'max-240x30')

    def get_parent(self, obj):
        return get_page_parent(obj)

class SurveyDetailSerializer(ModelSerializer):
    org = SerializerMethodField()
    demos_key = SerializerMethodField()
    tags = SerializerMethodField()
    assoc_commentary = SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id',
            'title',
            'slug',
            'url_path',
            'year',
            'month',
            'sample_number',
            'findings',
            'data_type',
            'national',
            'link',
            'file',
            'org',
            'demos_key',
            'assoc_commentary',
            'tags'
        ]
        read_only_fields = fields

    def get_assoc_commentary(self, obj):
        if obj.assoc_commentary is None:
            return []
        commentaries = []
        for i,s in enumerate(obj.assoc_commentary.all()):
            commentary = {
                'title': s.title
            }
            commentaries.append(commentary)
        return commentaries

    def get_org(self, obj):
        if obj.org is None:
            return []
        orgs = []
        for i,s in enumerate(obj.org.all()):
            org = {
                'title': s.title
            }
            orgs.append(org)
        return orgs

    def get_demos_key(self, obj):
        if obj.demos_key is None:
            return []
        demos_keys = []
        for i,s in enumerate(obj.demos_key.all()):
            key = {
                'title': s.title
            }
            demos_keys.append(key)
        return demos_keys

    def get_tags(self, obj):
        if obj.tags is None:
            return []
        tags = []
        for i,s in enumerate(obj.tags.all()):
            tag = {
                'title': s.title
            }
            tags.append(tag)
        return tags

def get_surveys_detail(homePage):
    children = homePage.get_children().type(Survey).live()
    surveys = []
    if children is not None:
        for c in children:
            surveys.append(SurveyDetailSerializer(c.specific).data)
    return surveys

def get_page_parent(page):
    parent_page = page.get_parent()
    if parent_page is not None:
        parent = {
          'title': parent_page.title,
          'url': parent_page.url
        }
        return parent
    else:
        return []