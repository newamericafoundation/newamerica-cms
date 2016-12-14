from __future__ import unicode_literals

from django.db import models
from django.apps import apps
from django.shortcuts import redirect
from datetime import datetime
from pytz import timezone
from django.db.models import Q

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition

from modelcluster.fields import ParentalKey

from programs.models import AbstractProgram, Program, Subprogram

from person.models import Person

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .blocks import ButtonBlock, IframeBlock, DatavizBlock
from mysite.blocks import GoogleMapBlock

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)

class CustomImage(AbstractImage):
    # Add any extra fields to image here

    source = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'source',
        'caption'
    )

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)

class HomePage(Page):
    """
    Model for the homepage for the website. In Wagtail's parent
    child structure, this is the most parent page.
    """
    subpage_types = [
    'OrgSimplePage',
    'programs.Program',
    'article.AllArticlesHomePage',
    'weekly.Weekly',
    'event.AllEventsHomePage',
    'conference.AllConferencesHomePage',
    'blog.AllBlogPostsHomePage',
    'book.AllBooksHomePage',
    'person.OurPeoplePage',
    'person.BoardAndLeadershipPeoplePage',
    'podcast.AllPodcastsHomePage',
    'policy_paper.AllPolicyPapersHomePage',
    'press_release.AllPressReleasesHomePage',
    'quoted.AllQuotedHomePage',
    'in_depth.AllInDepthHomePage',
    'JobsPage',
    'SubscribePage',
    'RedirectPage',
    ]

    # Up to four lead stories can be featured on the homepage.
    # Lead_1 will be featured most prominently.
    lead_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    lead_4 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Up to three featured stories to appear underneath
    # the lead stories. All of the same size and formatting.
    feature_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    feature_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    featured_stories = [feature_1, feature_2, feature_3]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                PageChooserPanel('lead_1'),
                PageChooserPanel('lead_2'),
                PageChooserPanel('lead_3'),
                PageChooserPanel('lead_4'),
            ],
            heading="Lead Stories",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                PageChooserPanel('feature_1'),
                PageChooserPanel('feature_2'),
                PageChooserPanel('feature_3'),
            ],
            heading="Featured Stories",
            classname="collapsible"
        ),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)

        # In order to apply different styling to main lead story
        # versus the other lead stories, we needed to separate them out
        context['other_lead_stories'] = []

        # Solution to account for null values for the stories
        # so that the div in the template wouldn't attempt to add styling to nothing
        if self.lead_2:
            context['other_lead_stories'].append(self.lead_2)
        if self.lead_3:
            context['other_lead_stories'].append(self.lead_3)
        if self.lead_4:
            context['other_lead_stories'].append(self.lead_4)

        # In order to preserve style, minimum and maximum of feature stories is 3
        # If there are less than 3 feature stories - none show up even if they're added.
        if self.feature_1 and self.feature_2 and self.feature_3:
            context['featured_stories'] = [
                self.feature_1, self.feature_2, self.feature_3
            ]
        else:
            context['featured_stories'] = []

        # uses get_model instead of traditional import to avoid circular import
        Event = apps.get_model('event', 'Event')

        eastern = timezone('US/Eastern')
        curr_time = datetime.now(eastern).time()
        curr_date = datetime.now(eastern).date()
        date_filter = Q(date__gt=curr_date) | (Q(date=curr_date) & Q(start_time__gte=curr_time))

        context['upcoming_events'] = Event.objects.live().filter(date_filter).order_by("date", "start_time")[:5]

        return context

class AbstractSimplePage(Page):
    """
    Abstract Simple page class that inherits from the Page model and
    creates simple, generic pages.
    """
    body = StreamField([
        ('introduction', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
        ('table', TableBlock()),
        ('button', ButtonBlock()),
        ('iframe', IframeBlock()),
    ])
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    class Meta:
        abstract = True


class RedirectPage(Page):
    """
    Redirect page class that inherits from the Page model and
    overrides the serve method to allow for redirects to pages
    external to the site.
    """

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    redirect_url = models.URLField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('redirect_url'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    def serve(self, request):
        return redirect(self.redirect_url, permanent=True)


class OrgSimplePage(AbstractSimplePage):
    """
    Simple Page at the organization level
    """
    parent_page_types = ['home.HomePage', 'OrgSimplePage']
    subpage_types = ['OrgSimplePage', 'home.RedirectPage']



class ProgramSimplePage(AbstractSimplePage):
    """
    Simple Page at the Program level
    """
    parent_page_types = ['programs.Program', 'ProgramSimplePage', 'programs.Subprogram']
    subpage_types = ['ProgramSimplePage', 'home.RedirectPage']


class JobsPage(OrgSimplePage):
    """
    Jobs Page at the organization level
    """
    parent_page_types = ['home.HomePage']


class SubscribePage(OrgSimplePage):
    """
    Subscribe Page at the organization level
    """
    parent_page_types = ['home.HomePage']

    newsletter_subscriptions = StreamField([
        ('subscription', blocks.StructBlock([
            ('title', blocks.CharBlock(required=True)),
            ('description', blocks.CharBlock(required=False, max_length=120)),
            ('id', blocks.CharBlock(required=True, max_length=6, help_text="Enter the unique campaign monitor ID")),
            ('checked_by_default', blocks.BooleanBlock(default=False, required=False, help_text="Controls whether subscription is checked by default on the Subscribe Page"))
        ], icon='placeholder'))
    ], null=True, blank=True)

    event_subscriptions = StreamField([
        ('subscription', blocks.StructBlock([
            ('title', blocks.CharBlock(required=True)),
            ('description', blocks.CharBlock(required=False, max_length=120)),
            ('id', blocks.CharBlock(required=True, max_length=6, help_text="Enter the unique campaign monitor ID")),
            ('checked_by_default', blocks.BooleanBlock(default=False, required=False, help_text="Controls whether subscription is checked by default on the Subscribe Page"))
        ], icon='placeholder'))
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('newsletter_subscriptions'),
        StreamFieldPanel('event_subscriptions')
    ]


class PostAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Authors
    """
    author = models.ForeignKey(Person, related_name="+")
    post = ParentalKey('Post', related_name='authors')

    panels = [
        FieldPanel('author'),
    ]


class PostProgramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Programs
    """

    program = models.ForeignKey(Program, related_name="+")
    post = ParentalKey('Post', related_name='programs')

    panels = [
        FieldPanel('program'),
    ]

    class meta:
        unique_together = (("program", "post"),)

    def __str__(self):
        return str(self.program) + "," + str(self.post)


class PostSubprogramRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Subprograms
    """

    subprogram = models.ForeignKey(Subprogram, related_name="+")
    post = ParentalKey('Post', related_name='subprograms')

    panels = [
        FieldPanel('subprogram'),
    ]
    class meta:
        unique_together = (("subprogram", "post"),)


class Post(Page):
    """
    Abstract Post class that inherits from Page
    and provides a model template for other content
    type models
    """

    subheading = models.TextField(blank=True, null=True)

    date = models.DateField("Post date")

    body = StreamField([
        ('introduction', blocks.RichTextBlock()),
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
        ('video', EmbedBlock(icon='media')),
        ('table', TableBlock()),
        ('button', ButtonBlock()),
        ('iframe', IframeBlock()),
        ('dataviz', DatavizBlock()),
        ('google_map', GoogleMapBlock())
    ])

    parent_programs = models.ManyToManyField(
        Program, through=PostProgramRelationship, blank=True)

    post_subprogram = models.ManyToManyField(
        Subprogram, through=PostSubprogramRelationship, blank=True)

    post_author = models.ManyToManyField(
        Person, through=PostAuthorRelationship, blank=True)

    story_excerpt = models.CharField(blank=True, null=True, max_length=140)

    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    data_project_external_script = models.CharField(blank=True, null=True, max_length=140, help_text="Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.")

    content_panels = Page.content_panels + [
        FieldPanel('subheading'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        InlinePanel('programs', label=("Programs")),
        InlinePanel('subprograms', label=("Subprograms")),
        InlinePanel('authors', label=("Authors")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('data_project_external_script'),
    ]

    is_creatable = False

    search_fields = Page.search_fields + [
        index.SearchField('body'),

        index.RelatedFields('parent_programs', [
            index.SearchField('name'),
        ]),

        index.RelatedFields('post_author', [
            index.SearchField('first_name'),
            index.SearchField('last_name'),
            index.SearchField('position_at_new_america'),
        ]),
    ]

    def get_context(self, request):
        context = super(Post, self).get_context(request)
        context['authors'] = self.authors.order_by('pk')

        return context

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program - post relationship is
        captured even if the user does not select it.
        """
        super(Post, self).save(*args, **kwargs)

        program_title = self.get_ancestors()[2]
        program = Program.objects.get(
            slug=program_title.slug
        )

        if isinstance(program, AbstractProgram):
            relationship, created=PostProgramRelationship.objects.get_or_create(
                program=program, post=self
            )
            if created:
                relationship.save()

        if len(self.get_ancestors()) >= 5:
            subprogram_title = self.get_ancestors()[3]
            subprogram = Subprogram.objects.get(slug=subprogram_title.slug)

            if isinstance(subprogram, AbstractProgram):
                relationship, created=PostSubprogramRelationship.objects.get_or_create(
                    subprogram=subprogram, post=self
                )
                if created:
                    relationship.save()
