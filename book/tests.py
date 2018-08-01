from django.test import TestCase

from django.test import TestCase

from wagtail.tests.utils import WagtailPageTests
from wagtail.core.models import Page

from .models import Book, AllBooksHomePage, ProgramBooksPage

from home.models import HomePage, PostProgramRelationship

from programs.models import Program, Subprogram, BlogProject, BlogSeries

class BookTests(WagtailPageTests):
    """
    Testing the Book, AllBooksHomePage, and
    ProgramBooksPage models to confirm hierarchies
    between pages and whether it is possible to create
    pages where it is appropriate.

    """

    def setUp(self):
        self.login()
        self.root_page = Page.objects.get(id=1)
        self.home_page = self.root_page.add_child(instance=HomePage(
            title='New America')
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
        self.program_books_page = self.program_page_1.add_child(instance=ProgramBooksPage(title='OTI Books'))
        self.book = self.program_books_page.add_child(instance=Book(title='Test Book 1', date='2016-02-10'))


    # Test that a particular child Page can be created under
    # the appropriate parent Page
    def test_can_create_book_under_program_books_page(self):
        self.assertCanCreateAt(ProgramBooksPage, Book)

    def test_cannot_create_book_under_all_books_page(self):
        self.assertCanNotCreateAt(AllBooksHomePage, Book)

    def test_can_create_program_books_page_under_program(self):
        self.assertCanCreateAt(Program, ProgramBooksPage)


    # Test allowed parent page types
    def test_book_parent_page(self):
        self.assertAllowedParentPageTypes(Book, {
            ProgramBooksPage,
            BlogProject,
            BlogSeries
        })

    def test_program_book_parent_page(self):
        self.assertAllowedParentPageTypes(ProgramBooksPage, {Program, Subprogram})

    def test_all_books_parent_page(self):
        self.assertAllowedParentPageTypes(AllBooksHomePage, {HomePage})


    # Test allowed subpage types
    def test_book_subpages(self):
        self.assertAllowedSubpageTypes(Book, {})

    def test_program_book_subpages(self):
        self.assertAllowedSubpageTypes(ProgramBooksPage, {Book})

    def test_all_book_homepage_subpages(self):
        self.assertAllowedSubpageTypes(AllBooksHomePage, {})

    #Test that pages can be created with POST data
    def test_can_create_all_book_page_under_homepage(self):
        self.assertCanCreate(self.home_page, AllBooksHomePage, {
            'title':'All Books at New America',
            }
        )

    def test_can_create_program_books_page(self):
        self.assertCanCreate(self.program_page_1, ProgramBooksPage, {
            'title':'Program Blogs',
            }
        )


    # Test relationship between Book and one parent Program
    def test_book_has_relationship_to_one_program(self):
        book = Book.objects.first()
        self.assertEqual(book.parent_programs.all()[0].title, 'OTI')


    # Test you can create a Book with two parent Programs
    def test_book_has_relationship_to_two_parent_programs(self):
        book = Book.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(program=self.second_program, post=book)
        relationship.save()
        self.assertEqual(book.parent_programs.filter(title='Education').first().title, 'Education')


    # Test book can be deleted if attached to one Program
    def test_can_delete_book_with_one_program(self):
        book = Book.objects.first()
        book.delete()
        self.assertEqual(Book.objects.filter(title='Test Book 1').first(), None)
        self.assertNotIn(book, ProgramBooksPage.objects.filter(title='OTI Books').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(post=book).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(post=book, program=self.program_page_1).first(), None)


    # Test book can be deleted if attached to two Programs
    def test_can_delete_book_with_two_programs(self):
        book = Book.objects.first()
        relationship, created = PostProgramRelationship.objects.get_or_create(program=self.second_program, post=book)
        if created:
            relationship.save()
        book.delete()
        self.assertEqual(Book.objects.filter(title='Test Book 1').first(), None)
        self.assertNotIn(book, ProgramBooksPage.objects.filter(title='OTI Books').first().get_children())
        self.assertEqual(PostProgramRelationship.objects.filter(post=book, program=self.program_page_1).first(), None)
        self.assertEqual(PostProgramRelationship.objects.filter(post=book, program=self.second_program).first(), None)
