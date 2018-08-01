from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from test_factories import PostFactory

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram

from .models import OtherPost, ProgramOtherPostsPage, AllOtherPostsHomePage, OtherPostCategory


class OtherContentTests(WagtailPageTests):
    def setUp(self):
        self.login()

        self.home_page = PostFactory.create_homepage()
        self.all_other_posts_home = self.home_page.add_child(
            instance=AllOtherPostsHomePage(title='Other', slug='other-home')
        )

        self.program = PostFactory.create_program(home_page=self.home_page)

        self.other_posts = PostFactory.create_program_content(10,
            program=self.program,
            content_page_type=ProgramOtherPostsPage,
            post_type=OtherPost,
            content_page_data={
                'singular_title': 'Singular Title'
            }
        )

        self.other_posts_home = ProgramOtherPostsPage.objects.first()

    # Test that a child Page can be created under the appropriate
    # Parent Page
    def test_can_create_otherpost_under_program_otherpost_page(self):
        self.assertCanCreateAt(ProgramOtherPostsPage, OtherPost)

        self.assertCanCreateAt(Program, ProgramOtherPostsPage)

    def test_can_create_program_otherpost_page_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ProgramOtherPostsPage)

     # Test allowed parent Page types
    def test_otherpost_parent_page(self):
        self.assertAllowedParentPageTypes(
            OtherPost, {
                ProgramOtherPostsPage,
                OtherPostCategory
            }
        )

    def test_program_otherpost_parent_page(self):
        self.assertAllowedParentPageTypes(
            ProgramOtherPostsPage,
            {Program, Subprogram}
        )

    def test_all_otherpost_parent_page(self):
        self.assertAllowedParentPageTypes(
            AllOtherPostsHomePage,
            {HomePage}
        )

    # Test allowed subpage types
    def test_otherpost_subpages(self):
        self.assertAllowedSubpageTypes(OtherPost, {})

    def test_program_otherpost_subpages(self):
        self.assertAllowedSubpageTypes(ProgramOtherPostsPage, {
            OtherPost,
            OtherPostCategory
        })

    # Test that pages can be created with POST data
    def test_can_create_all_otherposts_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllOtherPostsHomePage, {
            'title': 'Other Posts'
            }
        )

    def test_can_create_program_otherposts_page(self):
        self.assertCanCreate(self.program, ProgramOtherPostsPage, {
            'title': 'Other Posts',
            'singular_title': 'Other Post'
            }
        )

    def test_otherposts_has_relationship_to_one_program(self):
        post = OtherPost.objects.first()
        self.assertEqual(post.parent_programs.all()[0].title, self.program.title)


    def test_otherpost_with_one_parent_program_can_be_deleted(self):
        title = self.other_posts[0].title
        post = OtherPost.objects.filter(
            title=title).first()
        post.delete()
        self.assertEqual(OtherPost.objects.filter(
            title=title).first(), None
        )
        self.assertNotIn(
            post,
            ProgramOtherPostsPage.objects.first().get_children()
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=post).first(), None
        )
        self.assertEqual(
            PostProgramRelationship.objects.filter(
                post=post,
                program=self.program).first(),
            None
        )
