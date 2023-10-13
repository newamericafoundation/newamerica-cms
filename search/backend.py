from wagtail.models import Page
from wagtail.search.backends.elasticsearch7 import (
    Elasticsearch7Mapping,
    Elasticsearch7SearchBackend,
    Elasticsearch7SearchQueryCompiler,
)
from wagtail.search.index import FilterField

from home.models import Post


class QueryCompiler(Elasticsearch7SearchQueryCompiler):
    def get_inner_query(self):
        query = super().get_inner_query()

        # Get name of date field from a model that has it, but other models may have this field too
        date_field_name = Elasticsearch7Mapping(Post).get_field_column_name(
            FilterField("date")
        )

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
                            "filter": {"exists": {"field": date_field_name}},
                            "gauss": {
                                date_field_name: {
                                    "origin": "now",
                                    "scale": "300d",
                                    "decay": 0.8,
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
                    ],
                }
            }

        return query


class SearchBackend(Elasticsearch7SearchBackend):
    query_compiler_class = QueryCompiler
