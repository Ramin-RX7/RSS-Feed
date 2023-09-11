from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import test,PodcastListView,PodcastView,PodcastEpisodeListView,PodcastEpisodeDetailView



urlpatterns = format_suffix_patterns([
    path("test/", test, name="test"),

    path('podcasts/', PodcastListView.as_view()),
    path('podcast/<int:pk>', PodcastView.as_view()),

    path('podcast/<int:rss_pk>/episodes/', PodcastEpisodeListView.as_view()),
    path('podcast/<int:rss_pk>/episode/<int:episode_nom>', PodcastEpisodeDetailView.as_view()),
])
