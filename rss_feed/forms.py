from django.db import models
from django.contrib.syndication.views import Feed
# from blog.models import BlogPage
from home.models import Post

class BlogsFeed(Feed):
    title = "My blog articles"
    link = "/blogs-feed/"
    description = "All of my blogs as they are published"

    def items(self):
        return Post.objects.live().order_by('-date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro
