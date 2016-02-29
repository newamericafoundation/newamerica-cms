from django.core.management.base import BaseCommand
from home.management.api.author_transfer_script import run

class Command(BaseCommand):
	help = """ 
	Transfers data from the old 
	New America database into the new database.
	"""

	def handle(self, *args, **options):
		run()