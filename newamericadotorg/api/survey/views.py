from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.generics import RetrieveAPIView
from programs.models import Subprogram
from survey.models import Survey
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .serializers import SurveyHomeSerializer, SurveyDetailSerializer

@method_decorator(cache_page(60 * 180), name='get')
class SurveyHomeDetail(RetrieveAPIView):
    queryset = Subprogram.objects.live()
    serializer_class = SurveyHomeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class SurveyDetail(RetrieveAPIView):
    queryset = Survey.objects.live()
    serializer_class = SurveyDetailSerializer
