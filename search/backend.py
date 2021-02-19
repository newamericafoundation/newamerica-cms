from django.utils import timezone

from wagtail.core.models import Page
from wagtail.search.backends.elasticsearch5 import Elasticsearch5SearchBackend, Elasticsearch5SearchQueryCompiler, Elasticsearch5Mapping
from wagtail.search.index import FilterField

from home.models import Post


class QueryCompiler(Elasticsearch5SearchQueryCompiler):
    def get_inner_query(self):
        query = super().get_inner_query()

        # Get name of date field from a model that has it, but other models may have this field too
        date_field_name = Elasticsearch5Mapping(Post).get_field_column_name(FilterField('date'))

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
                                    "origin": "now",
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


class SearchBackend(Elasticsearch5SearchBackend):
    query_compiler_class = QueryCompiler
