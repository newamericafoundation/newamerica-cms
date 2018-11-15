from __future__ import unicode_literals

from django.db import models
from django.apps import apps
from django.shortcuts import redirect
from datetime import datetime
from pytz import timezone
from django.db.models import Q

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import PageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.admin.edit_handlers import (
    FieldPanel, StreamFieldPanel, InlinePanel,
    PageChooserPanel, MultiFieldPanel)
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from modelcluster.fields import ParentalKey

from programs.models import AbstractProgram, Program, Subprogram

from person.models import Person

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from newamericadotorg.blocks import BodyBlock
from newamericadotorg.wagtailadmin.widgets import LocationWidget

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('description',)

from subscribe.models import SubscriptionSegment

class CustomImage(AbstractImage):
    # Add any extra fields to image here

    source = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'source',
        'caption'
    )

    def get_url(self):
            try:
                 return self.url
            except:
                 return None

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

## unnecessary with wagtail 1.10
# # Delete the source image file when an image is deleted
# @receiver(pre_delete, sender=CustomImage)
# def image_delete(sender, instance, **kwargs):
#     instance.file.delete(False)
#
#
# # Delete the rendition image file when a rendition is deleted
# @receiver(pre_delete, sender=CustomRendition)
# def rendition_delete(sender, instance, **kwargs):
#     instance.file.delete(False)

class SubscriptionHomePageRelationship(models.Model):
    subscription_segment = models.ForeignKey(SubscriptionSegment, related_name="+")
    program = ParentalKey('HomePage', related_name='subscriptions')
    alternate_title = models.TextField(blank=True)
    panels = [
        FieldPanel('subscription_segment'),
        FieldPanel('alternate_title')
    ]

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
    'weekly.AllWeeklyArticlesHomePage',
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
    'RedirectPage',
    'home.SubscribePage',
    'subscribe.SubscribePage',
    'programs.PublicationsPage',
    'report.AllReportsHomePage',
    'other_content.AllOtherPostsHomePage'
    ]

    down_for_maintenance = models.BooleanField(default=False)

    subscription_segments = models.ManyToManyField(
        SubscriptionSegment,
        through=SubscriptionHomePageRelationship,
        blank=True,
    )

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

    about_pages = StreamField([
        ('page', PageChooserBlock()),
    ], blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('about_pages')
    ]

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

        InlinePanel('subscriptions', label=("Subscription Segments")),
    ]

    settings_panels = Page.settings_panels + [FieldPanel('down_for_maintenance')]

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

        context['upcoming_events'] = Event.objects.live().public().filter(date_filter).order_by("date", "start_time")[:3]
        context['recent_publications'] = Post.objects.live().public().specific().not_type(Event).order_by("-date")[:4]

        return context

class AbstractSimplePage(Page):
    """
    Abstract Simple page class that inherits from the Page model and
    creates simple, generic pages.
    """
    body = StreamField(BodyBlock(required=False), blank=True, null=True)
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)
    custom_interface = models.BooleanField(default=False)
    story_image = models.ForeignKey(
        'home.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    data_project_external_script = models.CharField(blank=True, null=True, max_length=140, help_text="Specify the name of the external script file within the na-data-projects/projects AWS directory to include that script in the body of the document.")

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('data_project_external_script'),
        FieldPanel('custom_interface')
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
    parent_page_types = ['home.HomePage', 'OrgSimplePage', 'JobsPage']
    subpage_types = ['OrgSimplePage', 'home.RedirectPage']

    page_description = RichTextField(blank=True)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('page_description'),
        ]),
        StreamFieldPanel('body')
    ]

    def get_context(self, request):
        context = super(OrgSimplePage, self).get_context(request)
        if self.custom_interface == True:
            context['template'] = 'home/custom_simple_interface.html'
        else:
            context['template'] = 'post_page.html'

        return context

    class Meta:
        verbose_name = 'About Page'



class ProgramSimplePage(AbstractSimplePage):
    """
    Simple Page at the Program level
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['home.RedirectPage']

    def get_context(self, request):
        context = super(ProgramSimplePage, self).get_context(request)
        context['program'] = self.get_parent().specific

        return context

    class Meta:
        verbose_name = 'About Page'

class ProgramAboutHomePage(ProgramSimplePage):
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = [
        'home.ProgramAboutPage'
    ]

    class Meta:
        verbose_name = 'About Homepage'

    def get_context(self, request):
        context = super().get_context(request)
        context['program'] = self.get_parent().specific

        if getattr(request, 'is_preview', False):
            program_context = context['program'].get_context(request)
            context['initial_state'] = program_context['initial_state']
            context['initial_topics_state'] = program_context['initial_topics_state']

        return context

class ProgramAboutPage(ProgramSimplePage):
    parent_page_types = ['home.ProgramAboutHomePage']
    subpage_types = [
        'home.ProgramSimplePage'
    ]

    def get_context(self, request):
        context = super(ProgramSimplePage, self).get_context(request)
        context['program'] = self.get_parent().get_parent().specific

        if getattr(request, 'is_preview', False):
            program_context = context['program'].get_context(request)
            context['initial_state'] = program_context['initial_state']
            context['initial_topics_state'] = program_context['initial_topics_state']

        return context

class JobsPage(OrgSimplePage):
    """
    Jobs Page at the organization level
    """

    class Meta:
        verbose_name = 'Jobs Page'


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

    class Meta:
        verbose_name = 'Subscribe Page'


class PostAuthorRelationship(models.Model):
    """
    Through model that maps the many to many
    relationship between Post and Authors
    """
    author = models.ForeignKey(Person, related_name="+")
    post = ParentalKey('Post', related_name='authors')

    panels = [
        PageChooserPanel('author'),
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

    #def __str__(self):
        #return str(self.program) + "," + str(self.post)


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

class PostTopicRelationship(models.Model):
    topic = models.ForeignKey('issue.IssueOrTopic', related_name="+")
    post = ParentalKey('home.Post', related_name="topics")

    panels = [
        PageChooserPanel('topic', 'issue.IssueOrTopic')
    ]

class Location(models.Model):
    location = models.CharField(max_length=999)
    formatted_address = models.CharField(max_length=999,blank=True, null=True)
    street_number = models.CharField(max_length=999,blank=True, null=True)
    street = models.CharField(max_length=999,blank=True, null=True)
    city = models.CharField(max_length=999,blank=True, null=True)
    state_or_province = models.CharField(max_length=999,blank=True, null=True)
    zipcode = models.CharField(max_length=999,blank=True, null=True)
    county = models.CharField(max_length=999,blank=True, null=True)
    country = models.CharField(max_length=999,blank=True, null=True)
    latitude = models.CharField(max_length=999,blank=True, null=True)
    longitude = models.CharField(max_length=999,blank=True, null=True)

    post = ParentalKey(
        'Post',
        related_name='location',
        blank=True,
        null=True
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('location', widget=LocationWidget),
            FieldPanel('formatted_address', classname="disabled-input"),
            FieldPanel('street_number', classname="disabled-input field-col col6",),
            FieldPanel('street', classname="disabled-input field-col col6"),
            FieldPanel('county', classname="disabled-input field-col col6"),
            FieldPanel('zipcode', classname="disabled-input field-col col6"),
            FieldPanel('city', classname="disabled-input field-col col12"),
            FieldPanel('state_or_province', classname="disabled-input field-col col12"),
            FieldPanel('country', classname="disabled-input field-col col12"),
            FieldPanel('latitude', classname="disabled-input field-col col6"),
            FieldPanel('longitude', classname="disabled-input field-col col6"),
        ])
    ]

class Post(Page):
    """
    Abstract Post class that inherits from Page
    and provides a model template for other content
    type models
    """

    subheading = models.TextField(blank=True, null=True)

    date = models.DateField("Post date")

    body = StreamField(BodyBlock(required=False), blank=True, null=True)

    parent_programs = models.ManyToManyField(
        Program, through=PostProgramRelationship, blank=True)

    post_subprogram = models.ManyToManyField(
        Subprogram, through=PostSubprogramRelationship, blank=True)

    post_author = models.ManyToManyField(
        Person, through=PostAuthorRelationship, blank=True)

    post_topic = models.ManyToManyField(
        'issue.IssueOrTopic', through=PostTopicRelationship, blank=True)

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
        InlinePanel('topics', label=("Topics")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
        InlinePanel('location', label=("Locations"),)
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

        subprogram = self.get_ancestors().type(Subprogram)
        if subprogram:
            if isinstance(subprogram, AbstractProgram):
                relationship, created=PostSubprogramRelationship.objects.get_or_create(
                    subprogram=subprogram[0].specific, post=self
                )
                if created:
                    relationship.save()

class AbstractHomeContentPage(Page):
    """
    Convenience Class for querying all Content homepages
    """

    class Meta:
        abstract=True
