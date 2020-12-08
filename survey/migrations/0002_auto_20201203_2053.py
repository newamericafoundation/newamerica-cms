# Generated by Django 3.0.7 on 2020-12-04 01:53

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0052_pagelogentry'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0054_auto_20200810_1541'),
        ('person', '0013_auto_20200109_1646'),
        ('issue', '0003_auto_20180811_1539'),
        ('programs', '0015_auto_20181019_0632'),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BlogIndexPage',
            new_name='Survey',
        ),
    ]
