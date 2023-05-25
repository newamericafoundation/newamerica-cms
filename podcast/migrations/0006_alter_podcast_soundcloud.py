# Generated by Django 3.2.18 on 2023-04-21 21:15

from django.db import migrations
import wagtail.embeds.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0005_auto_20180718_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='soundcloud',
            field=wagtail.fields.StreamField([('soundcloud_embed', wagtail.embeds.blocks.EmbedBlock())], blank=True, null=True, use_json_field=True),
        ),
    ]