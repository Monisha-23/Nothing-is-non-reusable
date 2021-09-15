# Generated by Django 3.2.5 on 2021-09-14 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0032_auto_20210914_1503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopkeeper',
            name='collectors',
        ),
        migrations.AddField(
            model_name='company',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='company_volunteers', to='my_app.volunteer'),
        ),
        migrations.AddField(
            model_name='garbagecollecter',
            name='collector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='garbagecollector_collector', to='my_app.volunteer'),
        ),
        migrations.AddField(
            model_name='shopkeeper',
            name='collector',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shopkeeper_collector', to='my_app.volunteer'),
        ),
        migrations.AlterField(
            model_name='garbagecollecter',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='garabgecollector_volunteers', to='my_app.volunteer'),
        ),
        migrations.AlterField(
            model_name='shopkeeper',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='shopkeeper_volunteers', to='my_app.volunteer'),
        ),
    ]
