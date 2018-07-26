from django.urls import reverse, include, path
from rest_framework import status
from rest_framework.test import APITestCase

class PostTests(APITestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_get_all(self):

        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.get(url, data, format='json')

        self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
