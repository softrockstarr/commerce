# Generated by Django 4.2 on 2023-05-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bid_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]