from django.db import models

from home.models import Post


class PressRelease(Post):
    """
    Press release class that inherits from the abstract
    Post model and creates pages for press releases.
    """
