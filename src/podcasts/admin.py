from django.contrib import admin,messages
from django.urls import reverse
from django.utils.html import format_html

from . import models
from .tasks import update_podcast




@admin.register(models.PodcastRSSPaths)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]

@admin.register(models.PodcastEpisodePaths)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]




class EpisodeRSSFilter(admin.SimpleListFilter):
    title = 'RSS'
    parameter_name = 'rss'
    def lookups(self, request, model_admin):
        return [(rss.name,rss.name) for rss in models.PodcastRSS.objects.all()]
    def queryset(self, request, queryset):
        if rss_name:=self.value():
            return queryset.filter(rss__name=rss_name)



@admin.register(models.PodcastEpisode)
class PodcastRSSAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    list_per_page = 30
    list_filter = [EpisodeRSSFilter,]
    actions = ["update_rss_action", ]
    search_fields = ["title"]






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
