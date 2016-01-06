# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpertPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='OurPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all People in NAF',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=150)),
                ('position', models.CharField(max_length=500)),
                ('bio', models.TextField(max_length=1000)),
                ('expert', models.BooleanField()),
                ('location', models.CharField(max_length=200)),
                ('photo', wagtail.wagtailcore.fields.StreamField([(b'photo', wagtail.wagtailimages.blocks.ImageChooserBlock())])),
                ('social_media', wagtail.wagtailcore.fields.StreamField([(b'twitter', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Twitter Handle', required=False)), (b'facebook', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Facebook Profile', required=False)), (b'youtube', wagtail.wagtailcore.blocks.URLBlock(help_text=b'YouTube Channel', required=False)), (b'google_plus', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Google+ Profile', required=False)), (b'linkedin', wagtail.wagtailcore.blocks.URLBlock(help_text=b'LinkedIn Profile', required=False)), (b'tumblr', wagtail.wagtailcore.blocks.URLBlock(help_text=b'Tumblr', required=False))])),
                ('role', models.CharField(max_length=50, choices=[(b'Board Member', b'Board Member'), (b'Staff', b'Staff'), (b'New America Fellow', b'New America Fellow'), (b'Program Fellow', b'Program Fellow')])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProgramPeoplePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Our People Page for Programs',
            },
            bases=('wagtailcore.page',),
        ),
    ]
