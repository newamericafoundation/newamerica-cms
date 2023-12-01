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
from person.models import (
    PersonProgramRelationship,
    PersonSubprogramRelationship,
    PersonTopicRelationship,
)
from programs.models import Program, Subprogram


class Command(BaseCommand):
    help = "Update the tagging on posts, people, and subpages from a given Program/Subprogram/Topic to a different Program."

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            help="The ID of a Program to which to re-tag people, posts, and pages.",
            required=True,
            type=int,
        )

        parser.add_argument(
            "--from",
            help="The ID of a Program, Subprogram, or Issue to untag people, pages, and posts from.",
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
        return f"{page.title} (id={page.pk}, type={page.page_type_display_name})"

    def display_plan(self):
        self.stdout.write(
            f"Found {len(self.posts_to_modify)} posts descended from {self.show_page(self.destination)}.\n- These posts will be saved."
        )
        self.stdout.write(
            f"\nFound {len(self.post_tags_to_remove)} posts tagged with {self.show_page(self.page_to_untag)}.\n- These tags will be updated to refer to {self.show_page(self.destination)}.\n- The relationship of these posts to {self.show_page(self.page_to_untag)} will be removed."
        )
        self.stdout.write(
            f"\nFound {len(self.person_tags_to_remove)} people tagged with {self.show_page(self.page_to_untag)}.\n- These people will be updated to belong to {self.show_page(self.destination)}.\n- The relationship of these people to {self.show_page(self.page_to_untag)} will be removed."
        )

    def execute_plan(self):
        for post in self.posts_to_modify:
            post.save()

        for tag in self.post_tags_to_remove:
            self.stdout.write(f"Updating tag for {tag.post!r}")
            PostProgramRelationship.objects.get_or_create(
                program=self.destination,
                post=tag.post,
            )
            tag.delete()
        for tag in self.person_tags_to_remove:
            self.stdout.write(f"Updating tag for {tag.person!r}")
            PersonProgramRelationship.objects.get_or_create(
                program=self.destination,
                person=tag.person,
                group=getattr(tag, 'group', None),
                fellowship_position=getattr(tag, 'fellowship_position', None),
                sort_order=getattr(tag, 'sort_order', None),
            )
            tag.delete()

    @transaction.atomic
    def handle(self, **options):
        from_pk = options["from"]
        to_pk = options["to"]

        try:
            self.destination = Page.objects.get(pk=to_pk).specific
        except Page.DoesNotExist:
            self.stdout.write(f"Page with ID {to_pk!r} does not exist. Exiting.")
            return

        self.posts_to_modify = Post.objects.descendant_of(self.destination)
        self.posts_to_modify.values_list("pk", flat=True)
        try:
            self.page_to_untag = Page.objects.get(pk=from_pk).specific
        except Page.DoesNotExist:
            self.stdout.write(f"Page with ID {from_pk!r} does not exist. Exiting.")
            return

        if isinstance(self.page_to_untag, Program):
            self.post_tags_to_remove = PostProgramRelationship.objects.filter(
                program__pk=self.page_to_untag.pk,
            )
            self.person_tags_to_remove = PersonProgramRelationship.objects.filter(
                program__pk=self.page_to_untag.pk,
            )
        elif isinstance(self.page_to_untag, Subprogram):
            self.post_tags_to_remove = PostSubprogramRelationship.objects.filter(
                subprogram__pk=self.page_to_untag.pk,
            )
            self.person_tags_to_remove = PersonSubprogramRelationship.objects.filter(
                subprogram__pk=self.page_to_untag.pk,
            )
        elif isinstance(self.page_to_untag, IssueOrTopic):
            self.post_tags_to_remove = PostTopicRelationship.objects.filter(
                topic__pk=self.page_to_untag.pk,
            )
            self.person_tags_to_remove = PersonTopicRelationship.objects.filter(
                topic__pk=self.page_to_untag.pk,
            )
        else:
            self.stdout.write(
                f"Page with id {from_pk!r} is of type {self.page_to_untag.page_type_display_name!r}, not program, subprogram, or topic. Exiting."
            )
            return

        if options.get("commit", False):
            self.display_plan()
            self.execute_plan()
            self.stdout.write("*** Database updated ***")
        else:
            self.display_plan()
            self.stdout.write(
                "\n*** Database not updated, pass option --commit to retag pages. ***"
            )
