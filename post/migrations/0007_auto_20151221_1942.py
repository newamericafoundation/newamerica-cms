# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0020_add_index_on_page_first_published_at'),
        ('post', '0006_articlehomepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Homepage for all Events',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterModelOptions(
            name='articlehomepage',
            options={'verbose_name': 'Homepage for all Articles'},
        ),
        migrations.AlterModelOptions(
            name='bookhomepage',
            options={'verbose_name': 'Homepage for all Books'},
        ),
    ]
