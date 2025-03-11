# Generated by Django 5.1.4 on 2025-01-24 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_historicaldata_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaldata',
            name='timeframe',
            field=models.CharField(choices=[('day', '1 Day'), ('week', '7 Days'), ('month', '1 Month'), ('year', '1 Year')], max_length=10),
        ),
    ]
