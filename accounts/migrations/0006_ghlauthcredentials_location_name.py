# Generated by Django 4.2.21 on 2025-05-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_opportunity_booked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='ghlauthcredentials',
            name='location_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
