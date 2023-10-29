# Generated by Django 4.0.10 on 2023-10-29 07:09

import apps.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedIn_url', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('twitter_url', models.CharField(blank=True, max_length=200, null=True)),
                ('psychometric_file', models.FileField(blank=True, null=True, upload_to='files/psychometric_files/', validators=[apps.models.validate_csv_extension])),
            ],
        ),
    ]
