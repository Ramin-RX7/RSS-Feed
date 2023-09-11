from django.shortcuts import render
from django.http import Http404

from rest_framework import generics




class EpisodeListView(generics.ListAPIView):
    model = None
    def get_queryset(self):
        rss_id = self.kwargs['rss_pk']
        queryset = self.model.objects.filter(rss__id=rss_id)
        return queryset

