from rest_framework.test import APITestCase

from test_factories import PostFactory

from report.models import Report, ReportsHomepage
from wagtail.core.blocks.stream_block import StreamValue
from report.blocks import ReportBody
from wagtail.core.rich_text import RichText

class ReportAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        home_page = PostFactory.create_homepage()

        program = PostFactory.create_program(home_page=home_page)

        report_home = PostFactory.create_program_content_page(
            program=program,
            content_page_type=ReportsHomepage
        )

        cls.report1 = PostFactory.create_content(1,
            content_page=report_home,
            post_type=Report
        )[0]

        cls.report2 = PostFactory.create_content(1,
            content_page=report_home,
            post_type=Report,
            post_data={
                'sections': [
                    ('section', {
                        'title': 'Section 1',
                        'body': StreamValue(
                                ReportBody(),
                                [
                                    ('heading', 'Subsection 1'),
                                    ('paragraph', RichText('<p></p>')),
                                    ('heading', 'Subsection 2'),
                                    ('paragraph', RichText('<p></p>'))
                                ]
                            )
                        }
                    ),
                    ('section', {
                        'title': 'Section 2',
                        'body': StreamValue(
                                ReportBody(),
                                [
                                    ('heading', 'Subsection 1'),
                                    ('paragraph', RichText('<p>Paragraph \{\{1\}\}</p>')),
                                    ('heading', 'Subsection 2'),
                                    ('paragraph', RichText('<p>Paragraph \{\{2\}\}</p>'))
                                ]
                            )
                        }
                    )
                ],
                'endnotes': [
                    ('endnote', { 'number': 1, 'note': RichText('<a>endnote 1</a>') }),
                    ('endnote', { 'number': 2, 'note': RichText('<a>endnote 2</a>') })
                ]
            }
        )[0]

    def test_get_report(self):
        url = '/api/report/%s/' % self.report1.id
        result = self.client.get(url)

        self.assertEquals(result.json()['title'], self.report1.title)

    def test_get_report_sections(self):
        url = '/api/report/%s/' % self.report2.id
        result = self.client.get(url)
        data = result.json()
        sections = data['sections']

        self.assertEquals(len(sections), 2)
        self.assertEquals(len(sections[0]['subsections']), 2)
        self.assertEquals(sections[1]['title'], 'Section 2')
        self.assertEquals(len(data['endnotes']), 2)
