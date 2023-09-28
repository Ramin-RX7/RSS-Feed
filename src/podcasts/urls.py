from django.urls import path,re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *



urlpatterns = format_suffix_patterns([
    path("test/", test, name="test"),

    path('podcasts/', PodcastListView.as_view()),
    path('podcast/<int:pk>', PodcastDetailView.as_view()),

    path('podcast/<int:rss_pk>/episodes/', PodcastEpisodeListView.as_view()),
    path('podcast/<int:rss_pk>/episode/<int:episode_nom>', PodcastEpisodeDetailView.as_view()),

    path('recommended/<str:method>/', PodcastRecommendationView.as_view()),

    # re_path(r'podcast/test/(?P<pk>\d*)', PodcastTest.as_view(),),
    # re_path(r'podcast/test/(?P<episode_nom>\d*)', PodcastTest.as_view(),),
])
