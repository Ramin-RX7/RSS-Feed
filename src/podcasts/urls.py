from django.urls import path

from .views import test


urlpatterns = [
    path("test/", test, name="test"),

    path('podcasts/', PodcastListView.as_view()),
    path('podcast/<int:pk>', PodcastView.as_view()),

