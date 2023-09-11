from django.shortcuts import render
from django.http import Http404

from rest_framework import generics




class EpisodeListView(generics.ListAPIView):
    model = None
    def get_queryset(self):
        rss_id = self.kwargs['rss_pk']
        queryset = self.model.objects.filter(rss__id=rss_id)
        return queryset



class EpisodeDetailView(generics.RetrieveAPIView):
    model = None

    @property
    def queryset(self):
        return self.model.objects.all()

    def get_object(self):
        rss_id = self.kwargs['rss_pk']
        queryset = self.queryset.filter(rss__id=rss_id)
        episode_nom = self.kwargs['episode_nom']
        if 0 <= episode_nom < queryset.count():
            return queryset[episode_nom]
        raise Http404("Episode not found.")
