from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey


# Abstract Program class that inherits from Page and provides template
class AbstractProgram(Page):
    name = models.CharField(max_length=100, help_text='Name of Program')
    location = models.NullBooleanField(
        help_text='Select if location based program i.e. New America NYC'
    )
    description = models.TextField()

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

    # Carousel of pages to feature on the landing page
    feature_carousel = StreamField([
        ('page', PageChooserBlock()),
    ], blank=True)

    about_us_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    # Story excerpt and story image fields are to provide information
    # about the program or subprogram if they are featured on a homepage
    # or program landing page
    story_excerpt = models.CharField(blank=True, null=True, max_length=500)

    story_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        FieldPanel('story_excerpt'),
        ImageChooserPanel('story_image'),
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
        StreamFieldPanel('feature_carousel'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name', classname='full title'),
        FieldPanel('location'),
        FieldPanel('description'),
        PageChooserPanel('about_us_page', 'home.ProgramSimplePage'),
    ]

    def get_context(self, request):
        context = super(AbstractProgram, self).get_context(request)

        context['other_lead_stories'] = []

        if self.lead_2:
            context['other_lead_stories'].append(self.lead_2)
        if self.lead_3:
            context['other_lead_stories'].append(self.lead_3)
        if self.lead_4:
            context['other_lead_stories'].append(self.lead_4)

        if self.feature_1 and self.feature_2 and self.feature_3:
            context['featured_stories'] = [
                self.feature_1, self.feature_2, self.feature_3
            ]
        else:
            context['featured_stories'] = []

        return context

    def get_experts(self):
        """ Return a list of experts in a program """
        return self.person_set.filter(expert=True).order_by('-title')

    def get_subprograms(self):
        """ Return a list of subprograms in a program """
        return self.get_children().type(Subprogram)

    class Meta:
        abstract = True


# Programs model which creates programs
class Program(AbstractProgram):
    parent_page_types = ['home.HomePage']

    program_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    sidebar_menu_initiatives_and_projects_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    sidebar_menu_our_work_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    sidebar_menu_about_us_pages = StreamField([
        ('Item', PageChooserBlock()),
    ], blank=True)

    content_panels = AbstractProgram.content_panels + [
        ImageChooserPanel('program_logo'),
    ]

    promote_panels = AbstractProgram.promote_panels + [
        StreamFieldPanel('sidebar_menu_initiatives_and_projects_pages'),
        StreamFieldPanel('sidebar_menu_our_work_pages'),
        StreamFieldPanel('sidebar_menu_about_us_pages'),
    ]

    def get_context(self, request):
        context = super(Program, self).get_context(request)
        
        return context

    class Meta:
        ordering = ('title',)


# Through relationship for Programs to Subprogram
class ProgramSubprogramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    subprogram = ParentalKey('Subprogram', related_name='programs')
    panels = [
        FieldPanel('program'),
    ]


# Subprograms models which when instantiated can be linked to multiple programs
class Subprogram(AbstractProgram):
    parent_page_types = ['programs.Program']
    parent_programs = models.ManyToManyField(
        Program,
        through=ProgramSubprogramRelationship,
        blank=True
    )
    content_panels = AbstractProgram.content_panels + [
        InlinePanel('programs', label=("Programs")),
    ]

    def get_template(self, request):
        return 'programs/program.html'

    class Meta:
        verbose_name = "Subprogram/Initiative Page"
        ordering = ('title',)

    def save(self, *args, **kwargs):
        """
        This save method overloads the wagtailcore Page save method in
        order to ensure that the parent program relationship is
        captured even if the user does not select it
        """
        super(Subprogram, self).save(*args, **kwargs)
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(
            slug=program_title.slug
        )

        if isinstance(program, AbstractProgram):
            relationship, created=ProgramSubprogramRelationship.objects.get_or_create(
                program=program, 
                subprogram=self
            )
            if created:
                relationship.save()
