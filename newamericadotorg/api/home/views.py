from rest_framework.generics import RetrieveAPIView

from home.models import OrgSimplePage

from .serializers import HomeDetailSerializer

class HomeDetail(RetrieveAPIView):
    queryset = OrgSimplePage.objects.live()
    serializer_class = HomeDetailSerializer
