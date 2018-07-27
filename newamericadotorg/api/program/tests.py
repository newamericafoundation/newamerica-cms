from rest_framework.test import APITestCase

from test_factories import PostFactory

from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage
from issue.models import IssueOrTopic

class ProgramAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = home_page.add_child(instance=Program(
            **PostFactory.program_data()
        ))

        program.save()

        subprogram = program.add_child(instance=Subprogram(
            **PostFactory.program_data()
        ))

        subprogram.save()
