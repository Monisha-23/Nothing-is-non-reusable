# Generated by Django 3.2.5 on 2021-09-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0017_auto_20210913_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apply',
            name='job_detail',
        ),
        migrations.AddField(
            model_name='apply',
            name='job_description',
            field=models.TextField(default='Job Description'),
        ),
        migrations.AddField(
            model_name='apply',
            name='job_title',
            field=models.CharField(default='Job Title', max_length=224),
        ),
        migrations.AddField(
            model_name='apply',
            name='posted_by',
            field=models.CharField(default='Posted By', max_length=224),
        ),
    ]
