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
    queryset = PodcastRSS.objects.all()
    serializer_class = PodcastRSSSerializer

class PodcastDetailView(generics.RetrieveAPIView):
    queryset = PodcastRSS.objects.all()
    serializer_class = PodcastRSSSerializer




class PodcastEpisodeListView(EpisodeListView):
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
