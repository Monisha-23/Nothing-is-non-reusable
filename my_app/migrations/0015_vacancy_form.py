# Generated by Django 3.2.5 on 2021-09-13 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0014_vacancy_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='form',
            field=models.URLField(default='https://www.google.com'),
        ),
    ]
