# Generated by Django 4.2.5 on 2023-10-21 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0003_podcastepisodepaths_route_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="podcastepisode",
            name="title",
            field=models.CharField(max_length=150),
        ),
    ]
