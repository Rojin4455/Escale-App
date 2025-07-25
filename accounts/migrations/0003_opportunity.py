# Generated by Django 4.2.21 on 2025-05-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_ghlauthcredentials_scope'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('opportunity_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('pipeline_name', models.CharField(blank=True, max_length=255, null=True)),
                ('pipeline_stage', models.CharField(blank=True, max_length=255, null=True)),
                ('lead_value', models.IntegerField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('assigned', models.CharField(blank=True, default='No Data', max_length=255, null=True)),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('lost_reason_id', models.CharField(blank=True, default='No Data', max_length=255, null=True)),
                ('lost_reason_name', models.CharField(default='No Data', max_length=255)),
                ('followers', models.TextField(default='No Data')),
                ('notes', models.TextField(default='No Data')),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('engagement_score', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('opportunity_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pipeline_stage_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pipeline_id', models.CharField(blank=True, max_length=255, null=True)),
                ('days_since_last_stage_change', models.CharField(blank=True, max_length=50, null=True)),
                ('days_since_last_status_change', models.CharField(blank=True, max_length=50, null=True)),
                ('days_since_last_updated', models.CharField(default='No Data', max_length=50)),
            ],
            options={
                'db_table': 'opportunity',
            },
        ),
    ]
