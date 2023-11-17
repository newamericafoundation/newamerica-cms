from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.core.models import Page

from home.models import (
    Post,
    PostProgramRelationship,
    PostSubprogramRelationship,
    PostTopicRelationship,
)
from issue.models import IssueOrTopic
from programs.models import Program, Subprogram


class Command(BaseCommand):
    help = "For all posts under a given Program/Subprogram/Topic, remove the tag for a second Program, and run the save method."

    def add_arguments(self, parser):
        parser.add_argument(
            "--parent",
            help="The ID of a parent Program, Subprogram, or Topic in which to find child posts",
            required=True,
            type=int,
        )

        parser.add_argument(
            "--remove",
            help="The ID of a Program to remove from the posts",
            required=True,
            type=int,
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Commit changes to the database",
        )

    def get_posts_for_program(self, pk):
        return PostProgramRelationship.objects.filter(
            program__pk=pk,
        )

    def get_posts_for_subprogram(self, pk):
        return PostSubprogramRelationship.objects.filter(
            subprogram__pk=pk,
        )

    def get_posts_for_topic(self, pk):
        return PostTopicRelationship.objects.filter(
            topic__pk=pk,
        )

    def show_page(self, page):
        return f'{page.title} (id={page.pk}, type={page.page_type_display_name})'

    def display_plan(self):
        parent_page = self.parent
        self.stdout.write(f"Found {len(self.posts_to_modify)} posts descended from {self.show_page(parent_page)}.\n- These posts will be saved.")
        self.stdout.write(f"\nFound {len(self.tags_to_remove)} of these posts tagged with {self.show_page(self.page_to_untag)}.\n- These tags will be removed.")

    def execute_plan(self):
        for post in self.posts_to_modify:
            post.save()

        for tag in self.tags_to_remove:
            self.stdout.write(f'Deleting {tag!r}')
            tag.delete()

    @transaction.atomic
    def handle(self, **options):
        parent_pk = options["parent"]

        try:
            self.parent = Page.objects.get(pk=parent_pk)
        except Page.DoesNotExist:
            self.stdout.write(f'Page with ID {parent_pk!r} does not exist. Exiting.')
            return

        self.posts_to_modify = Post.objects.descendant_of(self.parent)
        posts_to_modify_ids = self.posts_to_modify.values_list("pk", flat=True)
        remove_pk = options["remove"]
        try:
            self.page_to_untag = Page.objects.get(pk=remove_pk).specific
        except Page.DoesNotExist:
            self.stdout.write(f'Page with ID {remove_pk!r} does not exist. Exiting.')
            return

        if isinstance(self.page_to_untag, Program):
            self.tags_to_remove = PostProgramRelationship.objects.filter(
                program__pk=self.page_to_untag.pk,
                post_id__in=posts_to_modify_ids,
            )
        elif isinstance(self.page_to_untag, Subprogram):
            self.tags_to_remove = PostSubprogramRelationship.objects.filter(
                subprogram__pk=self.page_to_untag.pk,
                post_id__in=posts_to_modify_ids,
            )
        elif isinstance(self.page_to_untag, IssueOrTopic):
            self.tags_to_remove = PostTopicRelationship.objects.filter(
                topic__pk=self.page_to_untag.pk,
                post_id__in=posts_to_modify_ids,
            )
        else:
            self.stdout.write(
                f"Page with id {remove_pk!r} is of type {self.page_to_untag.page_type_display_name!r}, not program, subprogram, or topic. Exiting."
            )
            return

        if options.get("commit", False):
            self.display_plan()
            self.execute_plan()
            self.stdout.write('*** Database updated ***')
        else:
            self.display_plan()
            self.stdout.write(
                "\n*** Database not updated, pass option --commit to retag posts. ***"
            )
