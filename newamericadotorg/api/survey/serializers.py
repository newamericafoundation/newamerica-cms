from rest_framework.serializers import ModelSerializer, SerializerMethodField
from survey.models import Survey, SurveysHomePage
from programs.models import Subprogram
from newamericadotorg.api.author.serializers import AuthorSerializer
from wagtail.images.views.serve import generate_image_url

class SurveyHomeSerializer(ModelSerializer):
    survey_home_page = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = ['id', 'title', 'survey_home_page', 'seo_title', 'name', 'url_path']

    def get_survey_home_page(self, obj):
        return get_survey_homepage(obj)

class SurveysHomePageSerializer(ModelSerializer):
    surveys = SerializerMethodField()
    page_author = SerializerMethodField()
    partner_logo = SerializerMethodField()

    class Meta:
        model = SurveysHomePage
        fields = ['id', 'title', 'url_path', 'about', 'methodology', 'page_author', 'surveys', 'partner_logo', 'subheading']
        depth = 1
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

class SurveyDetailSerializer(ModelSerializer):

    class Meta:
        model = Survey
        depth = 1
        fields = [
            'id',
            'title',
            'slug',
            'url_path',
            'seo_title',
            'subheading',
            'description',
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

def get_survey_homepage(page):
    homePage = page.get_children().type(SurveysHomePage).live().first()
    if homePage is not None:
        surveyHomePage = SurveysHomePageSerializer(homePage.specific).data
        return surveyHomePage
    else:
        return []

def get_surveys_detail(homePage):
    children = homePage.get_children().type(Survey).live()
    surveys = []
    if children is not None:
        for c in children:
            surveys.append(SurveyDetailSerializer(c.specific).data)
    return surveys
