from django.shortcuts import render,HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from core.parser import *
from core.views import EpisodeListView,EpisodeDetailView
from accounts.auth_backends import JWTAuthBackend
from .models import PodcastRSS,PodcastEpisode
from .serializers import PodcastRSSSerializer,PodcastEpisodeSerializer
from .utils import get_recommended_podcasts



def test(request):
    test = PodcastRSS.objects.all()
    return render(request, "test.html", context={"test":test})






class PodcastListView(generics.ListAPIView):
    """
    List Podcasts.

    A JSON response containing a list of podcasts.

    Response Schema:
    ```
        [
            {
                "title": str,
                "email": str,
                "owner": str,
                "summary": str,
                "image": str,
                "host": str,
                "keywords": [str, ...],
                "explicit": bool,
                "copyright": str,
                "language": str,
                "link": str
            },
            ...
        ]
    ```
    """
    queryset = PodcastRSS.objects.all()
    serializer_class = PodcastRSSSerializer



class PodcastDetailView(generics.RetrieveAPIView):
    """
    Retrieve Podcast Details.

    Args:
        pk (int): The primary key of the podcast to retrieve.

    Returns:
        Response: A JSON response containing the details of the specified podcast.

    Response Schema:
    ```
        {
            "title": str,
            "email": str,
            "owner": str,
            "summary": str,
            "image": str,
            "host": str,
            "keywords": [str, ...],
            "explicit": bool,
            "copyright": str,
            "language": str,
            "link": str
        }
    ```
    """
    queryset = PodcastRSS.objects.all()
    serializer_class = PodcastRSSSerializer




class PodcastEpisodeListView(EpisodeListView):
    """
    List Podcast Episodes.

    Args:
        podcast_id (int): The primary key of the podcast for which to list episodes.

    Returns:
        Response: A JSON response containing a list of podcast episodes.

    Response Schema:
    ```
        [
            {
                "title": str,
                "duration": str,
                "audio_file": str,
                "publish_date": str,
                "explicit": bool,
                "summary": str,
                "description": str,
                "guests": [str, ...],
                "keywords": [str, ...],
                "image": str
            },
            ...
        ]
    ```
    """
    model = PodcastEpisode
    serializer_class = PodcastEpisodeSerializer



class PodcastEpisodeDetailView(EpisodeDetailView):
    """
    Retrieve Podcast Episode Details.

    Args:
        request (HttpRequest): The HTTP request object.
        podcast_id (int): The primary key of the podcast.
        episode_number (int): The episode number to retrieve details for.

    Returns:
        Response: A JSON response containing details of the podcast episode.

    Response Schema:
        {
            "title": str,
            "duration": str,
            "audio_file": str,
            "publish_date": str,
            "explicit": bool,
            "summary": str,
            "description": str,
            "guests": [str, ...],
            "keywords": [str, ...],
            "image": str
        }
    """
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer



class PodcastRecommendationView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        podcasts = get_recommended_podcasts(user)
        return Response(podcasts)
