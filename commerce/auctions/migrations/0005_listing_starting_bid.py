# Generated by Django 4.0 on 2022-01-09 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_category_alter_listing_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
