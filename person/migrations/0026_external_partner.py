# Generated by Django 3.2.18 on 2024-04-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0025_auto_20230915_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(choices=[('Board Chair', 'Board Chair'), ('Board Member', 'Board Member'), ('Fellow', 'Fellow'), ('Central Staff', 'Central Staff'), ('Program Staff', 'Program Staff'), ('External Author/Former Staff', 'External Author'), ('External Partner', 'External Partner')], max_length=50),
        ),
    ]
