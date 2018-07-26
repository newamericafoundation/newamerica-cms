from rest_framework.serializers import ModelSerializer, SerializerMethodField
from wagtail.core.models import Page, ContentType

from programs.models import Program, Subprogram, Project, BlogProject, AbstractContentPage
from subscribe.models import SubscriptionSegment
from newamericadotorg.api.helpers import generate_image_url, get_content_type

class PostProgramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug'
        )

    def get_name(self, obj):
        return obj.title

class PostSubprogramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'url', 'slug'
        )

    def get_name(self, obj):
        return obj.title;

class SubscriptionSegmentSerializer(ModelSerializer):

    class Meta:
        model = SubscriptionSegment
        fields = (
            'id', 'title', 'ListID', 'SegmentID'
        )


class ProgramSubprogramSerializer(ModelSerializer):
    '''
    Nested under program serializer
    '''
    name = SerializerMethodField()
    type = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = Page
        fields = (
            'id', 'name', 'url', 'title', 'slug', 'type'
        )
    def get_name(self, obj):
        return obj.title

    def get_type(self, obj):
        t = type(obj.specific)
        if t == Project or t == BlogProject:
            return 'Project'

        return 'Initiative'
    def get_url(self, obj):
        if getattr(obj.specific, 'redirect_page', None):
            return obj.specific.redirect_page.url

        return obj.url

class ProgramSerializer(ModelSerializer):
    logo = SerializerMethodField()
    subprograms = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'title', 'description', 'url', 'logo', 'slug', 'subprograms', 'subscriptions'
        )

    def get_subscriptions(self, obj):
        segments = []
        for s in obj.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_title != '':
                seg['alternate_title'] = s.alternate_title
            segments.append(seg)

        if len(segments) == 0:
            return None
        return segments

    def get_subprograms(self, obj):
        if type(obj) is not Program:
            return None
        #horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(obj.get_children().type(Subprogram).live().in_menu(),many=True).data
        if len(subprograms)==0:
            return None
        return subprograms

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo

class StoryGridItemSerializer(ModelSerializer):
    content_type = SerializerMethodField()
    story_image = SerializerMethodField()
    story_excerpt = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()

    def get_story_excerpt(self, obj):
        return obj.specific.story_excerpt

    def get_story_image(self, obj):
        if 'is_lead' in self.context:
            return generate_image_url(obj.specific.story_image, 'fill-925x430')
        return generate_image_url(obj.specific.story_image, 'fill-600x460')

    def get_story_image_thumbnail(self, obj):
        if 'is_lead' in self.context:
            return generate_image_url(obj.specific.story_image, 'fill-32x15')
        return generate_image_url(obj.specific.story_image, 'fill-30x23')

    def get_content_type(self, obj):
        return get_content_type(obj)

    class Meta:
        model = Page
        fields = ('id', 'title', 'url', 'slug', 'content_type', 'story_image', 'story_excerpt', 'story_image_thumbnail')

class ProgramDetailSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    description = SerializerMethodField()
    subprograms = SerializerMethodField()
    logo = SerializerMethodField()
    content_types = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()
    topics = SerializerMethodField()
    about = SerializerMethodField()
    about_us_pages = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id', 'name', 'title', 'story_grid', 'description', 'url', 'subprograms', 'slug',
            'content_types', 'features', 'subpages', 'logo', 'about', 'about_us_pages',
            'subscriptions', 'topics', 'hide_subscription_card', 'subscription_card_text'
        )

    def get_story_grid(self, obj):
        grid = []
        if obj.lead_1:
            context = self.context.copy()
            context['is_lead'] = True
            grid.append(StoryGridItemSerializer(obj.lead_1.specific, context=context).data)
        if obj.lead_2:
            grid.append(StoryGridItemSerializer(obj.lead_2.specific, context=self.context).data)
        if obj.lead_3:
            grid.append(StoryGridItemSerializer(obj.lead_3.specific, context=self.context).data)
        if obj.lead_4:
            grid.append(StoryGridItemSerializer(obj.lead_4.specific, context=self.context).data)
        if obj.feature_1:
            grid.append(StoryGridItemSerializer(obj.feature_1.specific, context=self.context).data)
        if obj.feature_2:
            grid.append(StoryGridItemSerializer(obj.feature_2.specific, context=self.context).data)
        if obj.feature_3:
            grid.append(StoryGridItemSerializer(obj.feature_3.specific, context=self.context).data)

        return grid

    def get_description(self, obj):
        return obj.description or obj.story_excerpt or obj.search_description

    def get_subprograms(self, obj):
        #horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(obj.get_children().type(Subprogram).live().in_menu(),many=True).data
        if len(subprograms)==0:
            return None
        return subprograms

    def get_topics(self, obj):
        topics = obj.get_descendants().filter(content_type__model='issueortopic', depth=5).specific().live().count()
        if topics > 0:
            return True

        return False

    def get_content_types(self, obj):
        return get_program_content_types(obj.id)

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo

    def get_features(self, obj):
        features = []
        for i in range(3):
            f = 'features_' + str(i+1)
            if getattr(obj,f,None):
                features.append(getattr(obj,f).id)
        return features

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        if not obj.about_us_page:
            return None;
        return {
            'url': obj.about_us_page.url,
            'slug': obj.about_us_page.slug,
            'title': obj.about_us_page.title,
            'body': loader.get_template('components/post_body.html').render({ 'page': obj.about_us_page.specific })
        }

    def get_about_us_pages(self, obj):
        if not obj.sidebar_menu_about_us_pages:
            return None
        if len(obj.sidebar_menu_about_us_pages) == 0:
            return None

        about_us_pages = []
        for p in obj.sidebar_menu_about_us_pages:
            try:
                p = p.value.specific
            except:
                continue
            if p.title == 'About Us' or p.title == 'Our People' or not p.live:
                continue
            body = loader.get_template('components/post_body.html').render({ 'page': p })
            about_us_pages.append({ 'title': p.title, 'body': body, 'slug': p.slug })

        if len(about_us_pages) == 0:
            return None

        return about_us_pages

    def get_subscriptions(self, obj):
        segments = []
        for s in obj.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_title != '':
                seg['alternate_title'] = s.alternate_title
            segments.append(seg)

        if len(segments) == 0:
            return None
        return segments


class SubprogramProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = (
            'id', 'name', 'url', 'slug', 'title'
        )

class SubprogramSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    parent_programs = SerializerMethodField()
    content_types = SerializerMethodField()
    description = SerializerMethodField()
    leads = SerializerMethodField()
    features = SerializerMethodField()
    subpages = SerializerMethodField()
    about = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id', 'name', 'story_grid', 'parent_programs', 'url', 'slug', 'content_types',
             'description', 'leads', 'features', 'subpages', 'about', 'title', 'subscriptions',
             'hide_subscription_card', 'subscription_card_text'
        )

    def get_parent_programs(self, obj):
        parents = SubprogramProgramSerializer(obj.parent_programs, many=True).data
        if len(parents)==0:
            return None
        return parents

    def get_story_grid(self, obj):
        grid = []
        context = self.context
        if obj.template == 'simple_program.html':
            context['is_lead'] = True
        if obj.lead_1:
            lead_context = self.context.copy()
            lead_context['is_lead'] = True
            grid.append(StoryGridItemSerializer(obj.lead_1.specific, context=lead_context).data)
        if obj.lead_2:
            grid.append(StoryGridItemSerializer(obj.lead_2.specific, context=context).data)
        if obj.lead_3:
            grid.append(StoryGridItemSerializer(obj.lead_3.specific, context=context).data)
        if obj.lead_4:
            grid.append(StoryGridItemSerializer(obj.lead_4.specific, context=context).data)
        if obj.feature_1:
            grid.append(StoryGridItemSerializer(obj.feature_1.specific, context=context).data)
        if obj.feature_2:
            grid.append(StoryGridItemSerializer(obj.feature_2.specific, context=context).data)
        if obj.feature_3:
            grid.append(StoryGridItemSerializer(obj.feature_3.specific, context=context).data)

        return grid

    def get_content_types(self, obj):
        return get_program_content_types(obj)

    def get_description(self, obj):
        return obj.description or obj.story_excerpt

    def get_leads(self, obj):
        leads = []
        for i in range(4):
            l = 'lead_' + str(i+1)
            if getattr(obj,l,None):
                leads.append(getattr(obj,l).id)
        return leads

    def get_features(self, obj):
        features = []
        for i in range(3):
            f = 'features_' + str(i+1)
            if getattr(obj,f,None):
                features.append(getattr(obj,f).id)
        return features

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        if not obj.about_us_page: return None

        return {
            'url': obj.about_us_page.url,
            'slug': obj.about_us_page.slug,
            'title': obj.about_us_page.title,
            'body': loader.get_template('components/post_body.html').render({ 'page': obj.about_us_page.specific })
        }

    def get_subscriptions(self, obj):
        segments = []
        for s in obj.subscriptions.all():
            seg = SubscriptionSegmentSerializer(s.subscription_segment).data
            if s.alternate_name != '':
                seg['alternate_title'] = s.alternate_name
            segments.append(seg)

        if len(segments) == 0:
            return None
        return segments
