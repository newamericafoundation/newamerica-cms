from rest_framework.generics import RetrieveAPIView

from report.models import Report

from .serializers import ReportDetailSerializer

class ReportDetail(RetrieveAPIView):
    serializer_class = ReportDetailSerializer
    queryset = Report.objects.live()
