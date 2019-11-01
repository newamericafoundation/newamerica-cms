from django.utils import timezone

from wagtail.core.models import Page
from wagtail.search.backends.elasticsearch2 import Elasticsearch2SearchBackend, Elasticsearch2SearchQueryCompiler
from wagtail.search.index import FilterField


class QueryCompiler(Elasticsearch2SearchQueryCompiler):
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
