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
    list_display = ["__str__", "view_episodes", "link", "updated_at", "created_at",]
    autocomplete_fields = ["main_fields_path", "episode_attributes_path"]
    fields = ["name", "url", "main_fields_path", "episode_attributes_path"]
    readonly_fields = ('view_episodes',)
    actions = ["update_rss_action",]
    search_fields = ["name", "main_fields__title"]

    @admin.action(description="Update selected podcasts")
    def update_rss_action(self, request, queryset):
        for rss in queryset:
            update_podcast.delay(podcast_id=rss.id, explicit_request=True)
        self.message_user(
            request,
            'Update request for selected podcast has been sent',
            level=messages.SUCCESS
        )

    def link(self, obj):
        link = f'<a href="{obj.url}" target="_blank">View RSS</a>'
        return format_html(link)

    def view_episodes(self, obj):
        url = reverse(f'admin:{models.PodcastEpisode._meta.app_label}_{models.PodcastEpisode._meta.model_name}_changelist')
        link = f'<a href="{url}?rss__id__exact={obj.pk}">View Episodes</a>'
        return format_html(link)
    view_episodes.short_description = 'Episodes'
