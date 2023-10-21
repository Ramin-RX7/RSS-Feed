from django.urls import path,re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *



urlpatterns = format_suffix_patterns([
    path("test/", test, name="test"),

    path('podcasts/', PodcastListView.as_view(), name="podcast_list"),
    path('podcasts/update/', PodcastUpdateView.as_view({"post":"update_all"}), name="podcast_update_all"),
    path('podcast/<int:pk>/', PodcastDetailView.as_view({"get":"get"}), name="podcast_detail"),
    path('podcast/<int:pk>/notify/on/', PodcastDetailView.as_view({"get":"notify_on"}), name="podcast_notify_on"),
    path('podcast/<int:pk>/notify/off/', PodcastDetailView.as_view({"get":"notify_off"}), name="podcast_notify_off"),
    path('podcast/<int:pk>/subscribers/', PodcastDetailView.as_view({"get":"subscribers"}), name="podcast_subscribers"),
    path('podcast/<int:pk>/subscribe/', PodcastDetailView.as_view({"get":"subscribe"}), name="podcast_subscribe"),
    path('podcast/<int:pk>/unsubscribe/', PodcastDetailView.as_view({"get":"unsubscribe"}), name="podcast_unsubscribe"),
    path('podcast/<int:pk>/update/', PodcastUpdateView.as_view({"post":"update_single"}), name="podcast_update_single"),

    path('podcast/<int:rss_pk>/episode/<int:pk>/likes/', EpisodeDetailView.as_view({"get":"likes"}), name="episode_likes"),
    path('podcast/<int:rss_pk>/episode/<int:pk>/like/', EpisodeDetailView.as_view({"get":"like"}), name="episode_like"),
    path('podcast/<int:rss_pk>/episode/<int:pk>/unlike/', EpisodeDetailView.as_view({"get":"unlike"}), name="episode_unlike"),
    path('podcast/<int:rss_pk>/episode/<int:pk>/', EpisodeDetailView.as_view({"get":"get"}), name="episode_detail"),
    path('podcast/<int:rss_pk>/episode/<int:pk>/comment/', EpisodeDetailView.as_view({"post":"comment"}), name="episode_comment"),

    path('podcast/<int:rss_pk>/episodes/', PodcastEpisodeListView.as_view(), name="podcast_episodes"),

    path('recommended/<str:method>/', PodcastRecommendationView.as_view(), name="recommendation"),

])
