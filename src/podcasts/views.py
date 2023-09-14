from django.shortcuts import render,HttpResponse
from rest_framework import generics


from core.parser import *
from core.views import EpisodeListView,EpisodeDetailView
from .models import PodcastRSS,PodcastEpisode
from .serializers import PodcastRSSSerializer,PodcastEpisodeSerializer



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
    queryset = PodcastEpisode.objects.all()
    serializer_class = PodcastEpisodeSerializer



def create_new_episode(request, rss_pk, episode_nom):
    rss = PodcastRSS.objects.get(id=rss_pk)
    parser = EpisodeXMLParser(rss, PodcastEpisode)
    content = get_rss_content(rss)
    parser.create_new_episode(content["item"][episode_nom-1])
    return HttpResponse("done")
