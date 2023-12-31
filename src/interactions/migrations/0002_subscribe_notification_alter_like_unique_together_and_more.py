# Generated by Django 4.2.5 on 2023-09-30 00:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("podcasts", "0002_alter_podcastepisode_duration"),
        ("interactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscribe",
            name="notification",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name="like",
            unique_together={("user", "episode")},
        ),
        migrations.AlterUniqueTogether(
            name="subscribe",
            unique_together={("user", "rss")},
        ),
    ]
