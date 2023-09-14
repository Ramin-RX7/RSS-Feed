from django.contrib import admin

from . import models
from . import forms




@admin.register(models.PodcastEpisode)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]

@admin.register(models.PodcastRSSPaths)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]

@admin.register(models.PodcastEpisodePaths)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]



@admin.register(models.PodcastRSS)
class PodcastRSSAdmin(admin.ModelAdmin):
    autocomplete_fields = ["main_fields_path", "episode_attributes_path"]
    fields = ["name", "url", "main_fields_path", "episode_attributes_path"]
    # readonly_fields = ["title"]

    # def get_form(self, request, obj=None, **kwargs):
        # if obj is None:
            # return super().get_form()
        # else:
            # return forms.CreateRSSForm
