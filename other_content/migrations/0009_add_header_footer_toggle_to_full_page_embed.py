# Generated by Django 3.2.18 on 2025-02-05 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('other_content', '0008_add_full_page_embed'),
    ]

    operations = [
        migrations.AddField(
            model_name='fullpageembed',
            name='include_header_footer',
            field=models.BooleanField(default=True, help_text='If true, the header and footer will be included in the page.'),
        ),
    ]
