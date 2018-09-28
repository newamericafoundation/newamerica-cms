from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram, Project

from .models import PressRelease, AllPressReleasesHomePage, ProgramPressReleasesPage


class PressReleaseTests(WagtailPageTests):
    """
    Testing the PressRelease, AllPressReleasesHomePage, and
    ProgramPressReleasesPage models to confirm
    hierarchies between pages and
    whether it is possible to create
    pages where it is appropriate.

    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
        )
        self.all_press_releases_home_page = self.home_page.add_child(
            instance=AllPressReleasesHomePage(
                title='New America Press Releases'
            )
        )
        self.program_page_1 = self.home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                description='OTI',
                location=False,
                depth=3
            )
        )
        self.second_program = self.home_page.add_child(
            instance=Program(
            title='Education',
            name='Education',
            slug='education',
            description='Education',
            location=False,
            depth=3
            )
        )
        self.program_press_releases_page = self.program_page_1\
            .add_child(instance=ProgramPressReleasesPage(
                title='OTI Press Releases')
            )
        self.press_release = PressRelease(
            title='Press Release 1',
            slug='press-release-1',
            date='2016-02-10',
            depth=5
        )
        self.program_press_releases_page.add_child(
            instance=self.press_release)
        self.press_release.save()

    # Test that a child Page can be created under the appropriate
    # Parent Page
    def test_can_create_press_release_under_program_press_releases_page(self):
        self.assertCanCreateAt(ProgramPressReleasesPage, PressRelease)

    def test_can_create_program_press_releases_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramPressReleasesPage)

    def test_can_create_program_press_releases_page_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ProgramPressReleasesPage)

    # Test allowed parent Page types
    def test_press_release_parent_page(self):
        self.assertAllowedParentPageTypes(
            PressRelease, {ProgramPressReleasesPage}
        )

    def test_program_press_release_parent_page(self):
        self.assertAllowedParentPageTypes(
            ProgramPressReleasesPage,
            {Program, Subprogram, Project}
        )

    def test_all_press_releases_parent_page(self):
        self.assertAllowedParentPageTypes(
            AllPressReleasesHomePage,
            {HomePage}
        )

    # Test allowed subpage types
    def test_press_release_subpages(self):
        self.assertAllowedSubpageTypes(PressRelease, {})

    def test_program_press_release_subpages(self):
        self.assertAllowedSubpageTypes(
            ProgramPressReleasesPage,
            {PressRelease}
        )

    # Test that pages can be created with POST data
    def test_can_create_all_press_releases_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllPressReleasesHomePage, {
            'title': 'New America Press Releases2',
            }
        )

    def test_can_create_program_press_releases_page(self):
        self.assertCanCreate(self.program_page_1, ProgramPressReleasesPage, {
            'title': 'Our Program Press Releases',
            }
        )

    # Test relationship between press release and one Program
    def test_press_release_has_relationship_to_one_program(self):
        press_release = PressRelease.objects.first()
        self.assertEqual(press_release.parent_programs.all()[0].title, 'OTI')

    # Test you can create a press release with two parent Programs
    def test_press_release_has_relationship_to_two_parent_programs(self):
        press_release = PressRelease.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=press_release)
        relationship.save()
        self.assertEqual(
            press_release.parent_programs.filter(
                title='Education').first().title, 'Education'
        )

    # Test press release page with one parent Program can be deleted
    def test_press_release_with_one_parent_program_can_be_deleted(self):
        press_release = PressRelease.objects.filter(
            title='Press Release 1').first()
        press_release.delete()
        self.assertEqual(PressRelease.objects.filter(
            title='Press Release 1').first(), None
        )
        self.assertNotIn(
            press_release,
            ProgramPressReleasesPage.objects.filter(
                title='OTI Press Releases').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=press_release).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=press_release,
                program=self.program_page_1).first(),
            None
        )

    # Test Press Release page with two parent Programs can be deleted
    def test_press_release_with_two_parent_programs_can_be_deleted(self):
        press_release = PressRelease.objects.filter(
            title='Press Release 1').first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program,
            post=press_release
            )
        if created:
            relationship.save()
        press_release.delete()
        self.assertEqual(PressRelease.objects.filter(
            title='Press Release 1').first(), None
        )
        self.assertNotIn(
            press_release,
            ProgramPressReleasesPage.objects.filter(
                title='OTI Press Releases').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=press_release,
                program=self.program_page_1).first(),
            None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=press_release,
                program=self.second_program).first(), None
        )
