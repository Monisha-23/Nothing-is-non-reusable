# Generated by Django 3.2.5 on 2021-09-13 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0020_alter_apply_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='garbage_collected',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
