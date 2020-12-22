from rest_framework.serializers import ModelSerializer, SerializerMethodField
from survey.models import Survey, ProgramSurveysPage, Commentary
from programs.models import Subprogram

class SurveyHomeSerializer(ModelSerializer):
    survey_home_page = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = ('__all__')

    def get_survey_home_page(self, obj):
        return get_survey_homepage(obj)

class ProgramSurveysPageSerializer(ModelSerializer):
    surveys = SerializerMethodField()

    class Meta:
        model = ProgramSurveysPage
        fields = '__all__'

    def get_surveys(self, obj):
        return get_surveys_detail(obj)

class SurveyDetailSerializer(ModelSerializer):
    survey_commentary = SerializerMethodField()

    class Meta:
        model = Survey
        depth = 2
        fields = '__all__'

    def get_survey_commentary(self, obj):
        return get_survey_commentary_detail(obj)

class CommentarySerializer(ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'

def get_survey_homepage(page):
    homePage = page.get_children().type(ProgramSurveysPage).live().first()
    if homePage is not None:
        surveyHomePage = ProgramSurveysPageSerializer(homePage).data
        return surveyHomePage
    else:
        return None

def get_surveys_detail(homePage):
    children = homePage.get_children().type(Survey).live()
    surveys = []
    if children is not None:
        for c in children:
            surveys.append(SurveyDetailSerializer(c.specific).data)
    return surveys

def get_survey_commentary_detail(survey):
    commentary = CommentarySerializer(Commentary.objects.filter(assoc_surveys=survey.id).live().first().specific)
    if commentary is not None:
        return commentary.data
    else:
         return []
