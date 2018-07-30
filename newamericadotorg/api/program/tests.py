from rest_framework.test import APITestCase

from test_factories import PostFactory

from programs.models import Program, Subprogram, FeaturedProgramPage, FeaturedSubprogramPage
from issue.models import IssueOrTopic

class ProgramAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program()
        subprogram = PostFactory.create_subprogram(program=program)
        
