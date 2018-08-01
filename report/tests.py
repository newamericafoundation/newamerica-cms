from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from test_factories import PostFactory

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram, BlogProject, BlogSeries

from .models import Report, ReportsHomepage, AllReportsHomePage


class ReportTests(WagtailPageTests):
    def setUp(self):
        self.login()

        self.home_page = PostFactory.create_homepage()
        self.all_report_home = self.home_page.add_child(
            instance=AllReportsHomePage(title='Reports', slug='reports-home')
        )

        self.program = PostFactory.create_program(home_page=self.home_page)

        self.reports = PostFactory.create_program_content(10,
            program=self.program,
            content_page_type=ReportsHomepage,
            post_type=Report
        )

    # Test that a child Page can be created under the appropriate
    # Parent Page
    def test_can_create_report_under_program_report_page(self):
        self.assertCanCreateAt(ReportsHomepage, Report)

    def test_can_create_program_report_page_under_program(self):
        self.assertCanCreateAt(Program, ReportsHomepage)

    def test_can_create_program_report_page_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ReportsHomepage)

     # Test allowed parent Page types
    def test_report_parent_page(self):
        self.assertAllowedParentPageTypes(
            Report, {
                ReportsHomepage
            }
        )

    def test_program_report_parent_page(self):
        self.assertAllowedParentPageTypes(
            ReportsHomepage,
            {Program, Subprogram}
        )

    def test_all_report_parent_page(self):
        self.assertAllowedParentPageTypes(
            AllReportsHomePage,
            {HomePage}
        )

    # Test allowed subpage types
    def test_report_subpages(self):
        self.assertAllowedSubpageTypes(Report, {})

    def test_program_report_subpages(self):
        self.assertAllowedSubpageTypes(ReportsHomepage, {Report})

    # Test that pages can be created with POST data
    def test_can_create_all_reports_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllReportsHomePage, {
            'title': 'Reports',
            }
        )

    def test_can_create_program_report_page(self):
        self.assertCanCreate(self.program, ReportsHomepage, {
            'title': 'Reports',
            }
        )

    def test_report_has_relationship_to_one_program(self):
        report = Report.objects.first()
        self.assertEqual(report.parent_programs.all()[0].title, self.program.title)


    def test_report_with_one_parent_program_can_be_deleted(self):
        title = self.reports[0].title
        report = Report.objects.filter(
            title=title).first()
        report.delete()
        self.assertEqual(Report.objects.filter(
            title=title).first(), None
        )
        self.assertNotIn(
            report,
            ReportsHomepage.objects.first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=report).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=report,
                program=self.program).first(),
            None
        )
