# Generated by Django 4.2 on 2023-05-05 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_comment_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bids',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
