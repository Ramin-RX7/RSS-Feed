from django.shortcuts import render
from django.http import Http404

from rest_framework import generics
from rest_framework.response import Response

from interactions.models import Like




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

    def get_user(self, request):
        from accounts.auth_backends import JWTAuthBackend
        from rest_framework import exceptions
        try:
            return JWTAuthBackend().authenticate(request)[0]
        except exceptions.PermissionDenied:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if user:=self.get_user(request):
            instance.liked = Like.objects.filter(user=user, episode=instance).exists()
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data)
