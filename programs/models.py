from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey

#Abstract Program class that inherits from Page and provides template
class AbstractProgram(Page):
    name = models.CharField(max_length=100, help_text='Name of Program')
    location = models.NullBooleanField(help_text='Check box if this is a location based program i.e. New America NYC')
    description = StreamField([
        ('heading', blocks.CharBlock(classname='full title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon='image')),
    ])

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

    content_panels = Page.content_panels + [
        FieldPanel('name', classname='full title'),
        FieldPanel('location'),
        StreamFieldPanel('description'),
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

        context['featured_stories'] = [
            self.feature_1, self.feature_2, self.feature_3
        ]

        return context

    def get_experts(self):
        """ Return a list of experts in a program """
        return self.person_set.filter(expert=True).order_by('-name')

    class Meta:
        abstract = True


#Programs model which creates programs
class Program(AbstractProgram):
    parent_page_types = ['home.HomePage',]



#Through relationship for Programs to Subprogram
class ProgramSubprogramRelationship(models.Model):
    program = models.ForeignKey(Program, related_name="+")
    subprogram = ParentalKey('Subprogram', related_name='programs')
    panels = [
        FieldPanel('program'),
    ]


#Subprograms models which when instantiated can be linked to multiple programs
class Subprogram(AbstractProgram):
    parent_programs = models.ManyToManyField(Program, through=ProgramSubprogramRelationship, blank=True)
    content_panels = AbstractProgram.content_panels + [
        InlinePanel('programs', label=("Programs")),
    ]

    class Meta:
        verbose_name = "Subprogram/Initiative Page"

