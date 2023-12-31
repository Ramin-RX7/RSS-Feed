# Generated by Django 4.2.5 on 2023-09-28 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PodcastEpisodePaths",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("audio_file", models.CharField(max_length=100)),
                ("duration", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                ("publish_date", models.CharField(max_length=100)),
                ("explicit", models.CharField(blank=True, max_length=100, null=True)),
                ("summary", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("keywords", models.CharField(blank=True, max_length=100, null=True)),
                ("image", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PodcastMainFields",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("owner", models.CharField(max_length=50)),
                ("category", models.CharField(blank=True, max_length=75, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("image", models.CharField(max_length=300, null=True)),
                ("host", models.CharField(max_length=50, null=True)),
                ("keywords", models.TextField(blank=True, null=True)),
                ("explicit", models.CharField(max_length=100, null=True)),
                ("copyright", models.CharField(max_length=100, null=True)),
                ("language", models.CharField(max_length=25, null=True)),
                ("link", models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PodcastRSSPaths",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("owner", models.CharField(max_length=100)),
                ("category", models.CharField(blank=True, max_length=100, null=True)),
                ("summary", models.CharField(blank=True, max_length=100, null=True)),
                ("image", models.CharField(blank=True, max_length=100, null=True)),
                ("host", models.CharField(blank=True, max_length=100, null=True)),
                ("keywords", models.CharField(blank=True, max_length=100, null=True)),
                ("explicit", models.CharField(blank=True, max_length=100, null=True)),
                ("copyright", models.CharField(blank=True, max_length=100, null=True)),
                ("language", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PodcastRSS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=25, unique=True)),
                ("url", models.URLField()),
                (
                    "episode_attributes_path",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="podcasts.podcastepisodepaths",
                    ),
                ),
                (
                    "main_fields",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="podcasts.podcastmainfields",
                    ),
                ),
                (
                    "main_fields_path",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="podcasts.podcastrsspaths",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PodcastEpisode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=75)),
                ("duration", models.PositiveIntegerField()),
                ("audio_file", models.CharField(max_length=300)),
                ("publish_date", models.PositiveIntegerField()),
                ("explicit", models.CharField(blank=True, max_length=100, null=True)),
                ("summary", models.TextField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("keywords", models.CharField(blank=True, max_length=150, null=True)),
                ("image", models.CharField(max_length=300, null=True)),
                (
                    "rss",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="podcasts.podcastrss",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
