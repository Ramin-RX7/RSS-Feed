from django.db import models,transaction

from core.models import BaseModel
from core.parser import *




class PodcastEpisodePaths(models.Model):
    audio_file = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=100)

    explicit = models.CharField(max_length=100, null=True, blank=True)
    summary = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)
    # guests = models.CharField(max_length=100, null=True, blank=True)



class PodcastRSSPaths(models.Model):
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



class PodcastMainFields(models.Model):
    # RSS Main fields
    title = models.CharField(max_length=50)
    email = models.EmailField()
    owner = models.CharField(max_length=50)

    category = models.CharField(max_length=75, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, null=True)      # URLField
    host = models.CharField(max_length=50, null=True)
    keywords = models.TextField(null=True, blank=True)
    explicit = models.CharField(max_length=100, null=True)   # Boolean field
    copyright = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=25, null=True)
    link = models.URLField(null=True)



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
            with transaction.atomic():
                rss_parser = RSSXMLParser(self, PodcastMainFields)
                rss_parser.fill_rss()
                saved = super().save()
                episode_parser = EpisodeXMLParser(self, PodcastEpisode)
                episode_parser.create_all_episodes()
                return saved
            # raise SystemError()
        return super().save()

    # def __str__(self):
        # return f"{self.name} ({self.main_fields.title})"



class PodcastEpisode(BaseModel):
    rss = models.ForeignKey(PodcastRSS, on_delete=models.CASCADE)
    # Required fields
    title = models.CharField(max_length=75)
    duration = models.PositiveIntegerField()
    audio_file = models.CharField(max_length=300)     # URLField
    publish_date = models.PositiveIntegerField()
    # Optional fields
    explicit = models.CharField(max_length=100, blank=True, null=True)   # Boolean field
    summary = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    keywords = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=300, null=True)      # URLField
    # guests = models.CharField(max_length=100, null=True, blank=True)
    # guid
    def __str__(self) -> str:
        return f"{self.rss.main_fields.title} - {self.title}"
