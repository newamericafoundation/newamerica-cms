# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('home', '0004_auto_20160106_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllPressReleasesHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all Press Releases',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PressRelease',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='home.Post')),
                ('headline', models.TextField()),
                ('sub_headline', models.TextField()),
                ('attachment', wagtail.wagtailcore.fields.StreamField([(b'attachment', wagtail.wagtaildocs.blocks.DocumentChooserBlock(null=True, required=False))])),
            ],
            options={
                'abstract': False,
            },
            bases=('home.post',),
        ),
        migrations.CreateModel(
            name='ProgramPressReleasesPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Press Release Homepage for Program',
            },
            bases=('wagtailcore.page',),
        ),
    ]
