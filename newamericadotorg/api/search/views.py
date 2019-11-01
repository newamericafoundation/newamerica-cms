from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from wagtail.core.models import Page, PageViewRestriction
from wagtail.search.models import Query

from .serializers import SearchSerializer

class SearchList(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend,SearchFilter)

    def get_queryset(self):
        search = self.request.query_params.get('query', None)
        results = Page.objects.live().search(search, partial_match=False)
        query = Query.get(search)
        query.add_hit()

        # search queryset does not allow .public(). manually exclude restricted pages
        public_results =[]
        restrictions = PageViewRestriction.objects.all()
        for obj in results:
            private = False
            for restriction in restrictions:
                if obj.id == restriction.page.id or obj.is_descendant_of(restriction.page):
                    private = True
                    break

            if not private:
                public_results.append(obj)

        return public_results
