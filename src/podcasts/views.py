from django.shortcuts import render
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

class PodcastView(generics.RetrieveAPIView):
    queryset = PodcastRSS.objects.all()
    serializer_class = PodcastRSSSerializer




class PodcastEpisodeListView(EpisodeListView):
    model = PodcastEpisode
    serializer_class = PodcastEpisodeSerializer


