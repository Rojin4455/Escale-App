# Generated by Django 4.2.21 on 2025-05-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_opportunity_location_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('webhook_id', models.CharField(blank=True, null=True)),
            ],
        ),
    ]
