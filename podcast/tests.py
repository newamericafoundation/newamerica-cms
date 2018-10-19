from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from .models import Podcast, AllPodcastsHomePage, ProgramPodcastsPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram, Project

class PodcastTests(WagtailPageTests):
    """
    Testing the Podcast, AllPodcastsHomePage, and
    ProgramPodcastsPage models to confirm
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
        self.all_podcasts_home_page = self.home_page.add_child(
            instance=AllPodcastsHomePage(title="All Podcasts at New America!")
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
        self.program_podcasts_page = self.program_page_1.add_child(
            instance=ProgramPodcastsPage(
                title='OTI Podcasts')
        )
        self.podcast = self.program_podcasts_page.add_child(
            instance=Podcast(title='Podcast 1', date='2016-02-10')
        )

    # Test that a child Page can be created under
    # the appropriate parent Page
    def test_can_create_podcast_under_program_podcasts_page(self):
        self.assertCanCreateAt(ProgramPodcastsPage, Podcast)

    def test_can_create_program_podcasts_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramPodcastsPage)

    # Test allowed parent page types
    def test_podcast_parent_page(self):
        self.assertAllowedParentPageTypes(
            Podcast, {
                ProgramPodcastsPage
            }
        )

    def test_program_podcasts_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramPodcastsPage, {Program, Subprogram, Project})

    def test_all_podcasts_parent_page(self):
        self.assertAllowedParentPageTypes(AllPodcastsHomePage, {HomePage})

    # Test allowed subpage types
    def test_podcast_subpages(self):
        self.assertAllowedSubpageTypes(Podcast, {})

    def test_program_podcast_subpages(self):
        self.assertAllowedSubpageTypes(ProgramPodcastsPage, {Podcast})

    # Test that pages can be created with POST data
    def test_can_create_all_podcasts_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllPodcastsHomePage, {
            'title': 'All Podcasts at New America2',
            }
        )

    def test_can_create_program_podcasts_page(self):
        self.assertCanCreate(self.program_page_1, ProgramPodcastsPage, {
            'title': 'Our Program Podcasts',
            }
        )

    # Test relationship between podcast and one
    # Program
    def test_podcast_has_relationship_to_one_program(self):
        podcast = Podcast.objects.first()
        self.assertEqual(podcast.parent_programs.all()[0].title, 'OTI')

    # Test you can create a podcast with two parent Programs
    def test_podcast_has_relationship_to_two_parent_programs(self):
        podcast = Podcast.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program, post=podcast)
        relationship.save()
        self.assertEqual(
            podcast.parent_programs.filter(title='Education').first().title,
            'Education'
        )

    # Test Podcast page with one parent Program can be deleted
    def test_podcast_with_one_parent_program_can_be_deleted(self):
        podcast = Podcast.objects.filter(title='Podcast 1').first()
        podcast.delete()
        self.assertEqual(Podcast.objects.filter(
            title='Podcast 1').first(), None
        )
        self.assertNotIn(
            podcast,
            ProgramPodcastsPage.objects.filter(
                title='OTI Podcasts').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=podcast).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=podcast,
                program=self.program_page_1).first(),
            None
        )

    # Test Podcast page with two parent Programs can be deleted
    def test_podcast_with_two_parent_programs_can_be_deleted(self):
        podcast = Podcast.objects.filter(
            title='Podcast 1').first()
        relationship, created = PostProgramRelationship.objects.get_or_create(
            program=self.second_program,
            post=podcast
            )
        if created:
            relationship.save()
        podcast.delete()
        self.assertEqual(Podcast.objects.filter(
            title='Podcast 1').first(), None
        )
        self.assertNotIn(
            podcast,
            ProgramPodcastsPage.objects.filter(
                title='OTI Podcasts').first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=podcast,
                program=self.program_page_1).first(),
            None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=podcast,
                program=self.second_program).first(), None
        )
