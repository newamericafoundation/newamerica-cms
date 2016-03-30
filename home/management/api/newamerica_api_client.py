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


	def get_data(self, endpoint):
		data_url = self.api_url + endpoint

		while data_url:
			response = self.client.get(data_url).json()
			data_url = response.get('next')
			yield response


	def activate_program(self, program_id):
		programs_url = self.api_url + 'programs'
		self.client.get(programs_url)
		csrf = self.client.cookies['csrftoken']
		csrftoken_data = {'csrfmiddlewaretoken': csrf}
		headers = {'Referer': programs_url}
		login_attempt = self.client.post(
			programs_url+'/'+str(program_id)+'/activate',
			data=csrftoken_data,
			headers=headers)
		assert login_attempt.status_code == 200


	def get_posts(self):
		for program in self.client.get(self.api_url + 'programs').json():
			print(program)
			program_id = program['id']
			self.activate_program(program_id)
			for post_set in self.get_data('posts'):
				for post in post_set['results']:
					yield post


	def program_content(self, program_id):
		self.activate_program(program_id)
		for post_set in self.get_data('posts'):
				for post in post_set['results']:
					yield post
