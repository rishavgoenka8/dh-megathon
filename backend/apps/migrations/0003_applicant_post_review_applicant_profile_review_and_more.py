# Generated by Django 4.0.10 on 2023-10-29 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_applicant'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='post_review',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='profile_review',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='applicant',
            name='psychometric_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]