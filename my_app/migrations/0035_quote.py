# Generated by Django 3.2.5 on 2021-09-14 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0034_rename_collector_garbagecollecter_picker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Quotes',
            },
        ),
    ]
