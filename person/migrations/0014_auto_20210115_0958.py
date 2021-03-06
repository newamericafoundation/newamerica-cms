# Generated by Django 3.0.7 on 2021-01-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0013_auto_20200109_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='fellowship_year',
            field=models.IntegerField(blank=True, choices=[(2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999)], null=True),
        ),
        migrations.AlterField(
            model_name='personprogramrelationship',
            name='fellowship_year',
            field=models.IntegerField(blank=True, choices=[(2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999)], null=True),
        ),
        migrations.AlterField(
            model_name='personsubprogramrelationship',
            name='fellowship_year',
            field=models.IntegerField(blank=True, choices=[(2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999)], null=True),
        ),
    ]
