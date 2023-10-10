from django.urls import path,re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *



urlpatterns = format_suffix_patterns([
    path("test/", test, name="test"),

    path('podcasts/', PodcastListView.as_view()),
    path('podcasts/update/', PodcastUpdateView.as_view({"post":"update_all"})),
    path('podcast/<int:pk>/', PodcastDetailView.as_view()),
    path('podcast/<int:pk>/update/', PodcastUpdateView.as_view({"post":"update_single"})),

    path('podcast/<int:rss_pk>/episode/<int:pk>/likes/', EpisodeDetailView.as_view({"get":"likes"})),
    path('podcast/<int:rss_pk>/episode/<int:pk>/like/', EpisodeDetailView.as_view({"get":"like"})),
    path('podcast/<int:rss_pk>/episode/<int:pk>/unlike/', EpisodeDetailView.as_view({"get":"unlike"})),
    path('podcast/<int:rss_pk>/episode/<int:pk>/', EpisodeDetailView.as_view({"get":"get"})),

    path('podcast/<int:rss_pk>/episodes/', PodcastEpisodeListView.as_view()),

    path('recommended/<str:method>/', PodcastRecommendationView.as_view()),

])
