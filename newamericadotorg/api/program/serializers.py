from django.template import loader
from django.utils.functional import cached_property
from rest_framework.serializers import (
    BooleanField,
    CharField,
    IntegerField,
    ModelSerializer,
    ReadOnlyField,
    Serializer,
    SerializerMethodField,
)
from wagtail.models import Page

from home.models import ProgramAboutHomePage, ProgramAboutPage
from newamericadotorg.api.helpers import (
    generate_image_rendition,
    get_content_type,
    get_program_content_types,
    get_subpages,
)
from programs.models import Program, Project, Subprogram


class AboutPageSerializer(ModelSerializer):
    body = SerializerMethodField()

    class Meta:
        model = ProgramAboutHomePage
        fields = ('id', 'url', 'slug', 'body', 'title')

    def get_body(self, obj):
        if self.context.get('is_preview', False):
            obj = obj.get_latest_revision_as_object()
        return loader.get_template('components/post_body.html').render(
            {'page': obj}
        )


class PostProgramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Program
        fields = ('id', 'name', 'url', 'slug')

    def get_name(self, obj):
        return obj.title


class PostSubprogramSerializer(ModelSerializer):
    name = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = ('id', 'name', 'url', 'slug')

    def get_name(self, obj):
        return obj.title


class MailingListPlacementSerializer(Serializer):
    title = ReadOnlyField()
    checked_by_default = BooleanField()
    mailing_list_segment_id = IntegerField()


class ProgramSubprogramSerializer(ModelSerializer):
    '''
    Nested under program serializer
    '''

    name = SerializerMethodField()
    type = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = Page
        fields = ('id', 'name', 'url', 'title', 'slug', 'type')

    def get_name(self, obj):
        return obj.title

    def get_type(self, obj):
        if obj.specific.former:
            return 'Former'

        t = type(obj.specific)
        if t == Project:
            return 'Project'

        return 'Initiative'

    def get_url(self, obj):
        if getattr(obj.specific, 'redirect_page', None):
            return obj.specific.redirect_page.url

        return obj.url


class ProgramNavOptionsSerializer(Serializer):
    url_label_array = CharField(read_only=True)


class ProgramSerializer(ModelSerializer):
    logo = SerializerMethodField()
    subprograms = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Program
        fields = (
            'id',
            'name',
            'former',
            'title',
            'description',
            'url',
            'logo',
            'slug',
            'subprograms',
            'subscriptions',
            'nav_options',
        )

    def get_subscriptions(self, obj):
        segments = [
            MailingListPlacementSerializer(s).data for s in obj.get_subscription_segments()
        ]

        if len(segments) == 0:
            return None
        return segments

    def get_subprograms(self, obj):
        if type(obj) is not Program:
            return None
        # horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(
            obj.get_children().type(Subprogram).live().in_menu(), many=True
        ).data
        if len(subprograms) == 0:
            return None
        return subprograms

    def get_logo(self, obj):
        return ''
        return obj.desktop_program_logo


class FeaturedPageSerializer(ModelSerializer):
    id = SerializerMethodField()
    title = SerializerMethodField()
    url = SerializerMethodField()
    slug = SerializerMethodField()
    content_type = SerializerMethodField()
    story_image = SerializerMethodField()
    story_image_alt = SerializerMethodField()
    story_excerpt = SerializerMethodField()
    story_image_thumbnail = SerializerMethodField()

    def get_id(self, obj):
        return obj.page.id

    def get_title(self, obj):
        return obj.page.title

    def get_url(self, obj):
        return obj.page.url

    def get_slug(self, obj):
        return obj.page.slug

    def get_story_excerpt(self, obj):
        return getattr(obj.page.specific, 'story_excerpt', None)

    def get_story_image(self, obj):
        # return generate_image_url(obj.story_image, 'fill-600x460')
        story_image = (
            obj.featured_image
            if obj.featured_image
            else getattr(obj.page.specific, 'story_image', None)
        )
        if not story_image:
            return None

        img = generate_image_rendition(story_image, 'width-600')
        if img:
            return {'width': img.width, 'height': img.height, 'url': img.url}
        return None

    def get_story_image_alt(self, obj):
        return getattr(obj.page.specific, 'story_image_alt', None)

    def get_story_image_thumbnail(self, obj):
        # return generate_image_url(obj.story_image, 'fill-30x23')
        story_image = (
            obj.featured_image
            if obj.featured_image
            else getattr(obj.page.specific, 'story_image', None)
        )
        if not story_image:
            return None

        img = generate_image_rendition(story_image, 'width-30')
        if img:
            return {'width': img.width, 'height': img.height, 'url': img.url}
        return None

    def get_content_type(self, obj):
        return get_content_type(obj.page.specific)

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'url',
            'slug',
            'content_type',
            'story_image',
            'story_excerpt',
            'story_image_thumbnail',
            'story_image_alt',
        )


class FeaturedLeadPageSerializer(FeaturedPageSerializer):
    def get_story_image(self, obj):
        story_image = (
            obj.featured_image
            if obj.featured_image
            else getattr(obj.page.specific, 'story_image', None)
        )
        if not story_image:
            return None

        # img = generate_image_rendition(story_image, 'fill-925x430')
        img = generate_image_rendition(story_image, 'fill-1600x744')
        if img:
            return {'width': img.width, 'height': img.height, 'url': img.url}
        return None

    def get_story_image_thumbnail(self, obj):
        story_image = (
            obj.featured_image
            if obj.featured_image
            else getattr(obj.page.specific, 'story_image', None)
        )
        if not story_image:
            return None

        img = generate_image_rendition(story_image, 'fill-32x15')
        if img:
            return {'width': img.width, 'height': img.height, 'url': img.url}
        return None


class ProgramDetailSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    description = SerializerMethodField()
    subprograms = SerializerMethodField()
    logo = SerializerMethodField()
    content_types = SerializerMethodField()
    subpages = SerializerMethodField()
    topics = SerializerMethodField()
    about = SerializerMethodField()
    subscriptions = SerializerMethodField()
    nav_options = ProgramNavOptionsSerializer()

    class Meta:
        model = Program
        fields = (
            'id',
            'name',
            'title',
            'story_grid',
            'description',
            'url',
            'subprograms',
            'slug',
            'content_types',
            'subpages',
            'logo',
            'about',
            'subscriptions',
            'topics',
            'hide_subscription_card',
            'subscription_card_text',
            'nav_options',
            'display_logo_as_name',
        )

    @cached_property
    def _featured_pages_ordering(self):
        """Returns the appropriate column specification to sort by,
        given either `asc` or `desc` in the query parameters for this
        request."""
        featured_pages_ordering_direction = self.context["request"].GET.get(
            "featured_pages_ordering",
            "desc",
        ).lower()
        return "sort_order" if featured_pages_ordering_direction == "asc" \
            else "-sort_order"

    def _get_related_featured_pages(self, base_obj):
        """Retrive the set of related featured pages in the correct order.

        We might be applying this query to either a `Program` or to a
        `Revision`.

        """
        return base_obj.featured_pages.all().order_by(self._featured_pages_ordering)

    def get_story_grid(self, obj):
        featured_pages = None
        pages = None

        if self.context.get('is_preview'):
            revision = obj.get_latest_revision_as_object()
            pages = self._get_related_featured_pages(revision)
            featured_pages = [rel for rel in pages]
        else:
            pages = self._get_related_featured_pages(obj)
            featured_pages = [rel for rel in pages[:7]]

        if len(featured_pages) == 0:
            return {'count': 0, 'pages': []}

        lead = FeaturedLeadPageSerializer(featured_pages.pop(0)).data
        return {
            'count': pages.count(),
            'pages': [lead]
            + FeaturedPageSerializer(featured_pages, many=True).data,
        }

    def get_description(self, obj):
        return obj.description or obj.story_excerpt or obj.search_description

    def get_subprograms(self, obj):
        # horribly inefficient. may have to add a ManyToManyField to Program??
        subprograms = ProgramSubprogramSerializer(
            obj.get_children().type(Subprogram).live().in_menu(), many=True
        ).data
        if len(subprograms) == 0:
            return None
        return subprograms

    def get_topics(self, obj):
        topics = (
            obj.get_descendants()
            .filter(content_type__model='issueortopic', depth=5)
            .specific()
            .live()
            .count()
        )
        if topics > 0:
            return True

        return False

    def get_content_types(self, obj):
        return get_program_content_types(obj.id)

    def get_logo(self, obj):
        image = generate_image_rendition(obj.desktop_program_logo)
        if image:
            return {
                'url': image.url,
                'alt': obj.desktop_program_logo_alt,
            }
        return None

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        about = ProgramAboutHomePage.objects.child_of(obj).live().first()
        if not about:
            return None

        about_page = AboutPageSerializer(about, context=self.context).data
        about_page['subpages'] = AboutPageSerializer(
            ProgramAboutPage.objects.descendant_of(about).live().in_menu(),
            context=self.context,
            many=True,
        ).data

        return about_page

    def get_subscriptions(self, obj):
        segments = [
            MailingListPlacementSerializer(s).data for s in obj.get_subscription_segments()
        ]

        if len(segments) == 0:
            return None
        return segments


class SubprogramProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = ('id', 'name', 'url', 'slug', 'title')


class SubprogramSerializer(ModelSerializer):
    story_grid = SerializerMethodField()
    parent_programs = SerializerMethodField()
    content_types = SerializerMethodField()
    description = SerializerMethodField()
    subpages = SerializerMethodField()
    about = SerializerMethodField()
    subscriptions = SerializerMethodField()

    class Meta:
        model = Subprogram
        fields = (
            'id',
            'name',
            'former',
            'story_grid',
            'parent_programs',
            'url',
            'slug',
            'content_types',
            'description',
            'subpages',
            'about',
            'title',
            'subscriptions',
            'hide_subscription_card',
            'subscription_card_text',
        )

    @cached_property
    def _featured_pages_ordering(self):
        featured_pages_ordering_direction = self.context["request"].GET.get(
            "featured_pages_ordering",
            "desc",
        ).lower()
        return "sort_order" if featured_pages_ordering_direction == "asc" \
            else "-sort_order"

    def _get_related_featured_pages(self, base_obj):
        """Retrive the set of related featured pages in the correct order.

        We might be applying this query to either a `Subprogram` or to
        a `Revision`.

        """
        return base_obj.featured_pages.all().order_by(self._featured_pages_ordering)

    def get_parent_programs(self, obj):
        parents = SubprogramProgramSerializer(
            obj.parent_programs, many=True
        ).data
        if len(parents) == 0:
            return None
        return parents

    def get_story_grid(self, obj):
        featured_pages = None
        pages = None

        if self.context.get('is_preview'):
            revision = obj.get_latest_revision_as_object()
            pages = self._get_related_featured_pages(revision)
            featured_pages = [rel for rel in pages]
        else:
            pages = self._get_related_featured_pages(obj)
            featured_pages = [rel for rel in pages]

        if len(featured_pages) == 0:
            return {'count': 0, 'pages': []}

        FeaturedSerializer = (
            FeaturedLeadPageSerializer
            if self.context.get('is_simple', False)
            else FeaturedPageSerializer
        )

        lead = FeaturedLeadPageSerializer(featured_pages.pop(0)).data
        return {
            'count': pages.count(),
            'pages': [lead]
            + FeaturedSerializer(featured_pages, many=True).data,
        }

    def get_content_types(self, obj):
        return get_program_content_types(obj)

    def get_description(self, obj):
        return obj.description or obj.story_excerpt

    def get_subpages(self, obj):
        return get_subpages(obj)

    def get_about(self, obj):
        about = ProgramAboutHomePage.objects.child_of(obj).live().first()
        if not about:
            return None

        about_page = AboutPageSerializer(about, context=self.context).data
        about_page['subpages'] = AboutPageSerializer(
            ProgramAboutPage.objects.child_of(about).in_menu().live(),
            many=True,
            context=self.context,
        ).data

        return about_page

    def get_subscriptions(self, obj):
        segments = [
            MailingListPlacementSerializer(s).data for s in obj.get_subscription_segments()
        ]

        if len(segments) == 0:
            return None
        return segments
