import requests

import os


class NAClient:
	def __init__(self):
		self.login_url = 'https://admin.newamerica.org/login/'
		self.api_url = 'https://admin.newamerica.org/api/'
		self.login_data = {
			'username': os.getenv('API_EMAIL'),
			'password': os.getenv('API_PASSW')
		}
		self.client = requests.Session()
		self.authenticate()


	def authenticate(self):
		headers = {'Referer': self.login_url}
		csrf = self.client.get(self.login_url).cookies['csrftoken']
		self.login_data['csrfmiddlewaretoken'] = csrf
		login_attempt = self.client.post(self.login_url, data=self.login_data, headers=headers)
		assert login_attempt.status_code == 200

	def get_data(self):
		endpoint = self.api_url

		while endpoint:
			response = self.client.get(endpoint).json()
			endpoint = response.get('next')
			yield response



