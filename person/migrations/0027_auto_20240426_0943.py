# Generated by Django 3.2.18 on 2024-04-26 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0026_external_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personprogramrelationship',
            name='group',
            field=models.CharField(blank=True, choices=[('Fellows', 'Fellows'), ('Former Fellows', 'Former Fellows'), ('Advisors', 'Advisors'), ('Contributing Staff', 'Contributing Staff'), ('Arizona State University Fellows', 'Arizona State University Fellows'), ('Former Arizona State University Fellows', 'Former Arizona State University Fellows'), ('CivicAI Advisory Trust', 'CivicAI Advisory Trust')], help_text="Set grouping for program's our people page", max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='personsubprogramrelationship',
            name='group',
            field=models.CharField(blank=True, choices=[('Fellows', 'Fellows'), ('Former Fellows', 'Former Fellows'), ('Advisors', 'Advisors'), ('Contributing Staff', 'Contributing Staff'), ('Arizona State University Fellows', 'Arizona State University Fellows'), ('Former Arizona State University Fellows', 'Former Arizona State University Fellows'), ('CivicAI Advisory Trust', 'CivicAI Advisory Trust')], help_text="Set grouping for subprogram's our people page", max_length=50, null=True),
        ),
    ]
