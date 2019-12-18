from datetime import date

from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from test_factories import PostFactory

from home.models import HomePage, CustomImage, PostAuthorRelationship
from in_depth.models import InDepthProject, AllInDepthHomePage

class InDepthTests(WagtailPageTests):
    def setUp(self):
        self.login()

        self.home_page = PostFactory.create_homepage()

        self.all_in_depth_home = self.home_page.add_child(
            instance=AllInDepthHomePage(title='In Depth Home Page')
        )

        self.indepthproject = self.all_in_depth_home.add_child(instance=InDepthProject(
            title="In Depth Project",
            date=str(date.today())
        ))
        self.indepthproject.save()

    def test_indepthproject_has_correct_ordered_date_string(self):
        self.assertEqual(
            self.indepthproject.ordered_date_string, f'{str(self.indepthproject.date)}-{self.indepthproject.id}'
        )

