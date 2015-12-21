from django.db import models

from post.models import Post


class BlogPost(Post):
    """
    Blog class that inherits from the abstract
    Post model and creates pages for blog posts.
    """