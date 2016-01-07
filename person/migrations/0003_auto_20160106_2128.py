# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_program'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='position',
        ),
        migrations.AddField(
            model_name='person',
            name='position_at_new_america',
            field=models.CharField(default=1, help_text=b'Position or Title at New America', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=wagtail.wagtailcore.fields.StreamField([(b'photo', wagtail.wagtailimages.blocks.ImageChooserBlock(icon=b'image'))]),
        ),
        migrations.AlterField(
            model_name='person',
            name='social_media',
            field=wagtail.wagtailcore.fields.StreamField([(b'twitter', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Twitter Handle', required=False, icon=b'user')), (b'facebook', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Facebook Profile', required=False, icon=b'user')), (b'youtube', wagtail.wagtailcore.blocks.URLBlock(help_text=b'YouTube Channel', required=False, icon=b'media')), (b'google_plus', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Google+ Profile', required=False, icon=b'user')), (b'linkedin', wagtail.wagtailcore.blocks.URLBlock(help_text=b'LinkedIn Profile', required=False, icon=b'user')), (b'tumblr', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Tumblr', required=False, icon=b'user'))]),
        ),
    ]
