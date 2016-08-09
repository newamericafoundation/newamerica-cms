from wagtail.tests.utils import WagtailPageTests
from wagtail.wagtailcore.models import Page, Site

from django.test import Client

from home.models import HomePage, PostProgramRelationship, PostAuthorRelationship

from programs.models import Program, Subprogram

from .models import PolicyPaper, AllPolicyPapersHomePage, ProgramPolicyPapersPage

from person.models import Person, OurPeoplePage


class PolicyPaperHierarchiesTests(WagtailPageTests):
    """
    Testing the PolicyPaper, AllPolicyPapersHomePage, and
    ProgramPolicyPapersPage models to confirm
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
        self.all_policy_papers_home_page = self.home_page.add_child(
            instance=AllPolicyPapersHomePage(title='New America Policy Papers')
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
        self.program_policy_papers_page = self.program_page_1\
            .add_child(instance=ProgramPolicyPapersPage(
                title='OTI Policy Papers')
            )
        self.policy_paper = PolicyPaper(
            title='Policy Paper 1',
            slug='policy-paper-1',
            date='2016-02-10',
            depth=5
        )
        self.program_policy_papers_page.add_child(
            instance=self.policy_paper)
        self.policy_paper.save()

    # Test that a child Page can be created under hte appropriate
    # Parent Page
    def test_can_create_policy_paper_under_program_policy_papers_page(self):
        self.assertCanCreateAt(ProgramPolicyPapersPage, PolicyPaper)

    def test_can_create_program_policy_papers_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramPolicyPapersPage)

    def test_can_create_program_policy_papers_page_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ProgramPolicyPapersPage)

    # Test allowed parent Page types
    def test_policy_paper_parent_page(self):
        self.assertAllowedParentPageTypes(
            PolicyPaper, {ProgramPolicyPapersPage}
        )

    def test_program_policy_paper_parent_page(self):
        self.assertAllowedParentPageTypes(
            ProgramPolicyPapersPage,
            {Program, Subprogram}
        )

    def test_all_policy_papers_parent_page(self):
        self.assertAllowedParentPageTypes(
            AllPolicyPapersHomePage,
            {HomePage}
        )

    # Test allowed subpage types
    def test_policy_paper_subpages(self):
        self.assertAllowedSubpageTypes(PolicyPaper, {})

    def test_program_policy_paper_subpages(self):
        self.assertAllowedSubpageTypes(ProgramPolicyPapersPage, {PolicyPaper})

    # Test that pages can be created with POST data
    def test_can_create_all_policy_papers_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllPolicyPapersHomePage, {
            'title': 'New America Policy Papers2',
            }
        )

    def test_can_create_program_policy_papers_page(self):
        self.assertCanCreate(self.program_page_1, ProgramPolicyPapersPage, {
            'title': 'Our Program Policy Papers',
            }
        )

    # Test relationship between policy paper and one Program
    def test_policy_paper_has_relationship_to_one_program(self):
        policy_paper = PolicyPaper.objects.first()
        self.assertEqual(policy_paper.parent_programs.all()[0].title, 'OTI')

    # Test you can create a policy paper with two parent Programs
    def test_policy_paper_has_relationship_to_two_parent_programs(self):
        policy_paper = PolicyPaper.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=policy_paper)
        relationship.save()
        self.assertEqual(
            policy_paper.parent_programs.filter(
                title='Education').first().title, 'Education'
        )

    # Test policy paper page with one parent Program can be deleted
    def test_policy_paper_with_one_parent_program_can_be_deleted(self):
        policy_paper = PolicyPaper.objects.filter(
            title='Policy Paper 1').first()
        policy_paper.delete()
        self.assertEqual(PolicyPaper.objects.filter(
            title='Policy Paper 1').first(), None
        )
        self.assertNotIn(
            policy_paper,
            ProgramPolicyPapersPage.objects.filter(
                title='OTI Policy Papers').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=policy_paper).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=policy_paper,
                program=self.program_page_1).first(),
            None
        )

    # Test Policy Paper page with two parent Programs can be deleted
    def test_policy_paper_with_two_parent_programs_can_be_deleted(self):
        policy_paper = PolicyPaper.objects.filter(
            title='Policy Paper 1').first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program,
            post=policy_paper
            )
        if created:
            relationship.save()
        policy_paper.delete()
        self.assertEqual(PolicyPaper.objects.filter(
            title='Policy Paper 1').first(), None
        )
        self.assertNotIn(
            policy_paper,
            ProgramPolicyPapersPage.objects.filter(
                title='OTI Policy Papers').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=policy_paper,
                program=self.program_page_1).first(),
            None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=policy_paper,
                program=self.second_program).first(), None
        )


class PolicyPaperIntegrationTests(WagtailPageTests):
    """
    Testing functionality of the various template tags
    used across the site.

    """
    def setUp(self):
        self.login()
        site = Site.objects.get()
        page = Page.get_first_root_node()
        home = HomePage(title='New America')
        home_page = page.add_child(instance=home)

        site.root_page = home
        site.save()

        # People objects to test template tags
        # that create byline and determine author order
        program_page_1 = home_page.add_child(
            instance=Program(
                title='OTI',
                name='OTI',
                slug='oti',
                description='OTI',
                location=False,
                depth=3
            )
        )
        program_page_1.save()

        our_people_page = home_page.add_child(
            instance=OurPeoplePage(
                title='Our People',
                depth=3,
            )
        )
        our_people_page.save()

        self.first_person = Person(
            title='First Person',
            slug='first-person',
            first_name='first',
            last_name='person',
            role='Central Staff',
            depth=4,
        )
        our_people_page.add_child(instance=self.first_person)

        # Using policy papers to test the other post types
        all_policy_papers_home_page = home_page.add_child(
            instance=AllPolicyPapersHomePage(title="Policy Papers")
        )

        program_policy_papers_page = program_page_1.add_child(
            instance=ProgramPolicyPapersPage(title='OTI Policy Papers', slug='oti-policy-papers')
        )
        self.policy_paper = PolicyPaper(
            title='Policy Paper 1',
            slug='policy-paper-1',
            date='2016-06-15',
            depth=5
        )
        program_policy_papers_page.add_child(instance=self.policy_paper)
        self.policy_paper.save()
        PostAuthorRelationship(author=self.first_person, post=self.policy_paper).save()
        all_policy_papers_home_page.save()