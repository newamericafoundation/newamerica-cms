from __future__ import unicode_literals

from django.db import models


class InDepthSection(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every Book in the Book model
    """
    parent_page_types = ['InDepthProject']
    subpage_types = []

    class Meta:
        verbose_name = "In-Depth Project Section"

class InDepthProject(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every Book in the Book model
    """
    parent_page_types = ['AllInDepthHomePage']
    subpage_types = ['InDepthSection']

    class Meta:
        verbose_name = "In-Depth Project"

class AllInDepthHomePage(Page):
    """
    A page which inherits from the abstract Page model and 
    returns every In Depth Page
    """
    parent_page_types = ['home.HomePage', ]
    subpage_types = ['InDepthProject']

    class Meta:
        verbose_name = "Homepage for all In-Depth Projects"