import os
import requests
import json
from rest_framework.views import APIView
from rest_framework.response import Response

class JobsList(APIView):
    def get(self, request, format=None):
        JAZZ_API_KEY = os.getenv('JAZZ_API_KEY')
        url = "https://api.resumatorapi.com/v1/jobs/status/open?apikey=%s" % JAZZ_API_KEY
        jobs = requests.get(url).json()
        return Response({
            'count': 0,
            'next': None,
            'previous': None,
            'results': jobs
        })
