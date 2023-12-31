from django.db import models, transaction

from core.models import BaseModel
from core.parser import *


class PodcastEpisodePaths(models.Model):
    route_name = models.CharField(max_length=50)
    audio_file = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=100)

    explicit = models.CharField(max_length=100, null=True, blank=True)
    summary = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'"{self.route_name}" episode router'


class PodcastRSSPaths(models.Model):
    route_name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)

    category = models.CharField(max_length=100, null=True, blank=True)
    summary = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    explicit = models.CharField(max_length=100, null=True, blank=True)
    copyright = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'"{self.route_name}" main field router'


class PodcastMainFields(models.Model):
    # RSS Main fields
    title = models.CharField(max_length=50)
    email = models.EmailField()
    owner = models.CharField(max_length=50)

    category = models.CharField(max_length=75, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, null=True, blank=True)  # XXX: URLField?
    host = models.CharField(max_length=50, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    explicit = models.CharField(max_length=100, null=True, blank=True)  # XXX: Boolean field
    copyright = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=25, null=True, blank=True)
    link = models.URLField(null=True, blank=True)


class PodcastRSS(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    url = models.URLField()
    # Main fields
    main_fields = models.OneToOneField(PodcastMainFields, models.PROTECT)
    # Main fields xml path
    main_fields_path = models.ForeignKey(PodcastRSSPaths, on_delete=models.CASCADE)
    # Episode fields xml path
    episode_attributes_path = models.ForeignKey(PodcastEpisodePaths, models.CASCADE)

    def update_episodes(self):
        parser = EpisodeXMLParser(self, PodcastEpisode)
        new_episodes = parser.update_episodes()
        return new_episodes

    def save(self, **kwargs):
        if not self.pk:
            return self.save_from_scratch()
        return super().save()

    def save_from_scratch(self):
        with transaction.atomic():
            rss_parser = RSSXMLParser(self, PodcastMainFields)
            rss_parser.fill_rss()
            saved = super().save()
            episode_parser = EpisodeXMLParser(self, PodcastEpisode)
            episode_parser.create_all_episodes()
            return saved

    def repair_database(self):
        PodcastEpisode.objects.filter(rss=self).delete()
        self.save_from_scratch()

    def __str__(self):
        return f"{self.name} ({self.main_fields.title})"


class PodcastEpisode(BaseModel):
    rss = models.ForeignKey(PodcastRSS, on_delete=models.CASCADE)

    # Required fields
    title = models.CharField(max_length=150)
    duration = models.PositiveIntegerField()
    audio_file = models.CharField(max_length=300)  # XXX: URLField
    publish_date = models.PositiveIntegerField()

    # Optional fields
    explicit = models.CharField(max_length=100, blank=True, null=True)  # XXX: Boolean field
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=300, null=True, blank=True)  # XXX: URLField

    # XXX: add guid field?

    def __str__(self) -> str:
        return f"{self.rss.main_fields.title} - {self.title}"
