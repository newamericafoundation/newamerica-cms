# Generated by Django 3.2.18 on 2023-10-20 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_auto_20230609_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='subscription_segments',
        ),
        migrations.DeleteModel(
            name='SubscriptionHomePageRelationship',
        ),
    ]