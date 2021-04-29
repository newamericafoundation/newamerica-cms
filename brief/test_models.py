from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.core import blocks
from wagtail.core.blocks.stream_block import StreamValue
from wagtail.core.rich_text import RichText
from wagtail.tests.utils import WagtailPageTests

from home.models import HomePage
from newamericadotorg.blocks import ResourceKit, Body, PanelsBlock
from programs.models import Program, Project, Subprogram
from test_factories import PostFactory

from .models import AllBriefsHomePage, Brief, ProgramBriefsPage


class BriefPagesHierarchy(WagtailPageTests):
    def test_can_create_brief_under_briefs_homepage(self):
        self.assertCanCreateAt(ProgramBriefsPage, Brief)

    def test_can_create_briefs_homepage_under_program(self):
        self.assertCanCreateAt(Program, ProgramBriefsPage)

    def test_can_create_briefs_homepage_under_subprogram(self):
        self.assertCanCreateAt(Subprogram, ProgramBriefsPage)

    def test_can_create_briefs_homepage_under_project(self):
        self.assertCanCreateAt(Project, ProgramBriefsPage)

    def test_can_create_all_briefs_page_under_homepage(self):
        self.assertCanCreateAt(HomePage, AllBriefsHomePage)

    def test_brief_can_only_have_one_parent_type(self):
        self.assertAllowedParentPageTypes(Brief, {ProgramBriefsPage})

    def test_brief_can_have_no_subpages(self):
        self.assertAllowedSubpageTypes(Brief, {})

    def test_program_brief_page_can_have_only_brief_subpages(self):
        self.assertAllowedSubpageTypes(ProgramBriefsPage, {Brief})

    def test_program_briefs_page_can_only_have_program_type_parents(self):
        self.assertAllowedParentPageTypes(
            ProgramBriefsPage, {Program, Subprogram, Project}
        )

    def test_all_briefs_can_only_have_homepage_parent(self):
        self.assertAllowedParentPageTypes(AllBriefsHomePage, {HomePage})


class BriefWordCountTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()
        program = PostFactory.create_program(home_page=home_page)

        cls.briefs_page = PostFactory.create_program_content_page(
            program=program,
            content_page_type=ProgramBriefsPage,
        )

        rvalue = StreamValue(
            ResourceKit().child_blocks['resources'],
            [
                (
                    'external_resource',
                    {
                        'name': 'Google',
                        'description': RichText('<p>Something something</p>'),
                        'resource': 'https://www.google.com',
                    },
                ),
            ],
        )

        panel_body_value = StreamValue(
            Body(),
            [
                ('introduction', RichText('<p>Hello panel</p>')),
                ('heading', 'Panel Heading'),
            ],
        )

        pvalue = StreamValue(
            PanelsBlock(), [('panel', {'title': 'Panel One', 'body': panel_body_value})]
        )

        cls.brief = PostFactory.create_content(
            1,
            content_page=cls.briefs_page,
            post_type=Brief,
            post_data={
                'body': [
                    ('introduction', RichText('<p>Hello world</p>')),
                    ('heading', 'Heading'),
                    ('paragraph', RichText('<p>Lorem Ipsum Dolor</p>')),
                    (
                        'resource_kit',
                        {
                            'title': 'Resources',
                            'description': 'Lorem Ipsum',
                            'resources': rvalue,
                        },
                    ),
                    ('panels', pvalue),
                ]
            },
        )[0]

    def test_word_count(self):
        self.assertEqual(self.brief.word_count(), 18)

    def test_word_count_limit(self):
        with self.assertRaises(ValidationError):
            PostFactory.create_content(
                1,
                content_page=self.briefs_page,
                post_type=Brief,
                post_data={
                    'body': [
                        ('introduction', RichText('<p>Hello world</p>')),
                        ('heading', 'Heading'),
                        ('paragraph', RichText('<p>Lorem Ipsum Dolor</p>')),
                        ('heading', 'Hello world ' * 5000),
                    ]
                },
            )
