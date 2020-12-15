from rest_framework.generics import RetrieveAPIView

from survey.models import Survey

from .serializers import SurveyDetailSerializer

class SurveyDetail(RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveyDetailSerializer

# class CommentaryDetail(RetrieveAPIView):
#     serializer_class = CommentaryDetailSerializer
#     queryset = Survey.objects.live()
