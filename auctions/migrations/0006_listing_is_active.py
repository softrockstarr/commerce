# Generated by Django 4.2 on 2023-04-26 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
