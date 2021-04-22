from django.test import TestCase
from wagtail.tests.utils import WagtailPageTests

from home.models import HomePage
from programs.models import Program, Subprogram, Project
from .models import Brief, ProgramBriefsPage, AllBriefsHomePage


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
        self.assertAllowedParentPageTypes(
            Brief,
            {ProgramBriefsPage}
        )

    def test_brief_can_have_no_subpages(self):
        self.assertAllowedSubpageTypes(Brief, {})

    def test_program_brief_page_can_have_only_brief_subpages(self):
        self.assertAllowedSubpageTypes(ProgramBriefsPage, {Brief})

    def test_program_briefs_page_can_only_have_program_type_parents(self):
        self.assertAllowedParentPageTypes(
            ProgramBriefsPage,
            {Program, Subprogram, Project}
        )

    def test_all_briefs_can_only_have_homepage_parent(self):
        self.assertAllowedParentPageTypes(
            AllBriefsHomePage,
            {HomePage}
        )
