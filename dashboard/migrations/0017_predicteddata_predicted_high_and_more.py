# Generated by Django 5.1.4 on 2025-02-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_alter_predicteddata_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='predicteddata',
            name='predicted_high',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='predicteddata',
            name='predicted_low',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='predicteddata',
            name='predicted_open_price',
            field=models.FloatField(default=0),
        ),
    ]
