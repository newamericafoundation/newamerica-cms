# Generated by Django 3.0.7 on 2021-01-09 01:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import multiselectfield.db.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0054_auto_20200810_1541'),
        ('person', '0014_auto_20210115_0958'),
        ('wagtailcore', '0052_pagelogentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Post')),
            ],
            options={
                'verbose_name': 'Insights & Analysis',
            },
            bases=('home.post',),
        ),
        migrations.CreateModel(
            name='Commented_Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Commentary')),
            ],
        ),
        migrations.CreateModel(
            name='DemographicKey',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Demographic Keys',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PageAuthorRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='person.Person')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='SurveyOrganization',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Survey Organizations',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveyTags',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name_plural': 'Survey Tags',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveyValuesIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'verbose_name': 'Surveyindex Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SurveysHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('about', wagtail.core.fields.RichTextField(blank=True, max_length=1500, verbose_name='About This Project')),
                ('subscribe', wagtail.core.fields.StreamField([('cta_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=200, required=False)), ('link_text', wagtail.core.blocks.CharBlock(max_length=200, required=False)), ('link_url', wagtail.core.blocks.CharBlock(max_length=200, required=False))]))], blank=True, null=True)),
                ('submissions', wagtail.core.fields.StreamField([('cta_block', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=50, required=False)), ('description', wagtail.core.blocks.TextBlock(max_length=200, required=False)), ('link_text', wagtail.core.blocks.CharBlock(max_length=200, required=False)), ('link_url', wagtail.core.blocks.CharBlock(max_length=200, required=False))]))], blank=True, null=True)),
                ('about_submission', wagtail.core.fields.RichTextField(blank=True, max_length=500)),
                ('subheading', models.CharField(blank=True, max_length=300)),
                ('methodology', wagtail.core.fields.RichTextField(blank=True, max_length=1500)),
                ('page_author', models.ManyToManyField(blank=True, through='survey.PageAuthorRelationship', to='person.Person')),
                ('partner_logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage')),
            ],
            options={
                'verbose_name': 'Surveys Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Post')),
                ('description', models.CharField(blank=True, help_text='A brief description of the survey. 500 chars max', max_length=500, null=True)),
                ('year', models.IntegerField(blank=True, default=2000, help_text='Year Survey was conducted.')),
                ('month', models.CharField(blank=True, choices=[(None, 'N/A'), ('Jan', 'January'), ('Feb', 'February'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'), ('Jun', 'June'), ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December')], default=None, help_text='Month Survey was conducted, if applicable.', max_length=3, null=True)),
                ('sample_number', models.IntegerField(blank=True, null=True)),
                ('findings', wagtail.core.fields.RichTextField(blank=True, max_length=12500, null=True)),
                ('data_type', multiselectfield.db.fields.MultiSelectField(choices=[('QUANT', 'Quantitative'), ('QUAL', 'Qualitative')], max_length=10)),
                ('national', models.BooleanField(default=True, help_text='Indicates whether the survey was nationally representative or not.', verbose_name='Nationally Representative?')),
                ('link', models.URLField(blank=True, help_text='Add a link to a webpage containing the survey details.', null=True, verbose_name='Link to Survey')),
                ('file', models.FileField(blank=True, help_text='Add a file containing the survey details.', null=True, upload_to='', verbose_name='Survey File')),
                ('assoc_commentary', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='surveys', through='survey.Commented_Survey', to='survey.Commentary', verbose_name='Associated Commentary')),
                ('demos_key', modelcluster.fields.ParentalManyToManyField(blank=True, default=False, help_text='Indexable demographic groups', to='survey.DemographicKey', verbose_name='Demographics Keys')),
                ('org', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='SurveyOrganization', to='survey.SurveyOrganization', verbose_name='Organization')),
                ('tags', modelcluster.fields.ParentalManyToManyField(blank=True, default=False, help_text='Select from available tags', to='survey.SurveyTags', verbose_name='Topics')),
            ],
            options={
                'verbose_name': 'Survey Reports',
            },
            bases=('home.post',),
        ),
        migrations.AddField(
            model_name='pageauthorrelationship',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='survey.SurveysHomePage'),
        ),
        migrations.AddField(
            model_name='commented_survey',
            name='survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='commentary',
            name='assoc_surveys',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, related_name='commentaries', through='survey.Commented_Survey', to='survey.Survey'),
        ),
    ]
