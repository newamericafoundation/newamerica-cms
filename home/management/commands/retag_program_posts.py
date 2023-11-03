from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import (
    PostProgramRelationship,
    PostSubprogramRelationship,
    PostTopicRelationship,
)
from programs.models import Program


class Command(BaseCommand):
    help = "Tag all posts from one program, subprogram, or topic onto a different program, subprogram, or topic."

    def add_arguments(self, parser):
        parser.add_argument(
            "--from",
            help="The slug of a Program, Subprogram, or Topic in which to find posts",
            required=True,
        )

        parser.add_argument(
            "--to",
            help="The slug of a Program to which to add posts",
            required=True,
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Commit changes to the database",
        )

    def get_posts_for_program(self, slug):
        return PostProgramRelationship.objects.filter(
            program__slug=slug,
        )

    def get_posts_for_subprogram(self, slug):
        return PostSubprogramRelationship.objects.filter(
            subprogram__slug=slug,
        )

    def get_posts_for_topic(self, slug):
        return PostTopicRelationship.objects.filter(
            topic__slug=slug,
        )

    def display_plan(self, container_type, posts, slug):
        self.stdout.write(f"Posts in {container_type} {slug}: {len(posts)}")

    @transaction.atomic
    def handle(self, **options):
        from_slug = options["from"]

        if post_rels := self.get_posts_for_program(from_slug):
            self.display_plan("Program", post_rels, from_slug)
        elif post_rels := self.get_posts_for_subprogram(from_slug):
            self.display_plan("Subprogram", post_rels, from_slug)
        elif post_rels := self.get_posts_for_topic(from_slug):
            self.display_plan("IssueOrTopic", post_rels, from_slug)
        else:
            self.stdout.write(
                f"No posts found for any program, subprogram, or topic with slug {from_slug!r}, aborting."
            )
            return

        to_slug = options["to"]
        try:
            program = Program.objects.get(slug=to_slug)
            self.stdout.write(f"Found program {program.title} with slug {to_slug!r}")
        except Program.DoesNotExist:
            self.stdout.write(f"No program found with slug {to_slug!r}, aborting.")
            return

        if options.get("commit", False):
            total_created = 0
            total_unchanged = 0

            for post_rel in post_rels:
                try:
                    ppr, created = PostProgramRelationship.objects.get_or_create(
                        program=program,
                        post=post_rel.post,
                    )
                except PostProgramRelationship.MultipleObjectsReturned:
                    created = False
                if created:
                    total_created += 1
                else:
                    total_unchanged += 1

            self.stdout.write(f"Updated post count: {total_created}")
            self.stdout.write(f"Posts already in program: {total_unchanged}")
        else:
            self.stdout.write(
                "Database not updated, pass option --commit to retag posts."
            )
