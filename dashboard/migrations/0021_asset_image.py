# Generated by Django 5.1.4 on 2025-02-12 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_alter_asset_percent_change_alter_asset_price_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='asset_images/'),
        ),
    ]
