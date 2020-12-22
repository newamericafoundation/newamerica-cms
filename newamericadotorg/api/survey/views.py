from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import RetrieveAPIView
from programs.models import Subprogram
from survey.models import Survey

from .serializers import SurveyHomeSerializer, SurveyDetailSerializer

class SurveyHomeDetail(RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SurveyHomeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class SurveyDetail(RetrieveAPIView):
    queryset = Survey.objects.live()
    serializer_class = SurveyDetailSerializer
