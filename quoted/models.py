from django.db import models

from home.models import Post


class Quoted(Post):
    """
    Quoted class that inherits from the abstract
    Post model and creates pages for Quoted pages where New 
    America was in the news.
    """