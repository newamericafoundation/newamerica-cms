# Generated by Django 3.2.18 on 2023-07-21 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0019_convert_sort_priority_to_integer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='sort_priority',
        ),
    ]