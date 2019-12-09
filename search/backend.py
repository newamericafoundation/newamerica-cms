from django.utils import timezone

from wagtail.core.models import Page
from wagtail.search.backends.elasticsearch2 import Elasticsearch2SearchBackend, Elasticsearch2SearchQueryCompiler
from wagtail.search.index import FilterField


class QueryCompiler(Elasticsearch2SearchQueryCompiler):
    # Taken from Elasticsearch 5 backend.
    # For some reason, the ES2 implementation doesn't like the way we're excluding private pages.
    def _connect_filters(self, filters, connector, negated):
        if filters:
            if len(filters) == 1:
                filter_out = filters[0]
            elif connector == 'AND':
                filter_out = {
                    'bool': {
                        'must': [
                            fil for fil in filters if fil is not None
                        ]
                    }
                }
            elif connector == 'OR':
                filter_out = {
                    'bool': {
                        'should': [
                            fil for fil in filters if fil is not None
                        ]
                    }
                }

            if negated:
                filter_out = {
                    'bool': {
                        'mustNot': filter_out
                    }
                }

            return filter_out

    def get_inner_query(self):
        query = super().get_inner_query()

        first_published_at_field_name = self.mapping.get_field_column_name(FilterField('first_published_at'))

        # If we're searching pages, add a function to the query to decrease
        # the score of older results
        if issubclass(self.queryset.model, Page):
            query = {
                "function_score": {
                    "query": query,
                    "functions": [
                        {
                            "gauss": {
                                first_published_at_field_name: {
                                    "origin": timezone.now().isoformat(),
                                    "scale": "300d",
                                    "decay": 0.8
                                }
                            }
                        }
                    ],
                    "score_mode": "multiply"
                }
            }

        return query


class SearchBackend(Elasticsearch2SearchBackend):
    query_compiler_class = QueryCompiler
