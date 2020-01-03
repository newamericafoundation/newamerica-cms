from django.utils import timezone

from wagtail.core.models import Page
from wagtail.search.backends.elasticsearch2 import Elasticsearch2SearchBackend, Elasticsearch2SearchQueryCompiler, Elasticsearch2Mapping
from wagtail.search.index import FilterField

from home.models import Post


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

        # Get name of date field from a model that has it, but other models may have this field too
        date_field_name = Elasticsearch2Mapping(Post).get_field_column_name(FilterField('date'))

        if issubclass(self.queryset.model, Page):
            query = {
                "function_score": {
                    "query": query,
                    "score_mode": "first",
                    "boost_mode": "multiply",
                    "functions": [
                        {
                            # For pages with a "date" filter field, this will be used
                            # to decrease the score of older results.
                            "filter": {
                                "exists": {
                                    "field": date_field_name
                                }
                            },
                            "gauss": {
                                date_field_name: {
                                    "origin": timezone.now().isoformat(),
                                    "scale": "300d",
                                    "decay": 0.8
                                }
                            },
                        },
                        {
                            # For pages that don't have a date field, return
                            # a score of 1 so that it doesn't affect the score
                            # returned by the query
                            "script_score": {
                                "script": "1",
                            }
                        },
                    ]
                }
            }

        return query


class SearchBackend(Elasticsearch2SearchBackend):
    query_compiler_class = QueryCompiler
