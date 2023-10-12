from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import (action,authentication_classes as auth_classes)


from core.parser import *
from core.views import EpisodeListView,EpisodeDetailView
from accounts.auth_backends import JWTAuthBackend
from accounts.models import User
from interactions.models import Like
from interactions.serializers import LikeSerializer
from .models import PodcastRSS,PodcastEpisode
from .serializers import PodcastRSSSerializer,PodcastEpisodeSerializer
from .utils import like_based_recomended_podcasts,subscription_based_recommended_podcasts
from .tasks import update_podcasts_episodes,update_podcast



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



class EpisodeDetailView(generics.RetrieveAPIView, viewsets.ViewSet):
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

    def get_user(self, request):
        if not (auth:=JWTAuthBackend().authenticate(request)):
            return Response({"details":"login required"}, status=status.HTTP_403_FORBIDDEN)
        user = auth[0]
        if user.is_authenticated:
            return user


    @action(detail=False)
    def likes(self, request, *args, **kwargs):
        qs = Like.objects.filter(episode=self.get_object())
        users = qs.values_list("user", flat=True)
        return Response({"users":users, "count":len(users)})

    @action(detail=True)
    def like(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is None:
            return Response({"details":"login required"}, status=status.HTTP_403_FORBIDDEN)
        episode = self.get_object()
        like,created = Like.objects.get_or_create(user=user, episode=episode)
        if created:
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"details":"already liked"}, status=status.HTTP_208_ALREADY_REPORTED)

    @action(detail=True)
    def unlike(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user is None:
            return Response({"details":"login required"}, status=status.HTTP_403_FORBIDDEN)
        like_qs = Like.objects.filter(user=user, episode=self.get_object())
        if not like_qs.exists():
            return Response({'detail': 'not liked yet'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # for like in like_qs:
        #     like.delete()
        like_qs.get().delete()
        return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_202_ACCEPTED)



class PodcastRecommendationView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    recommendations_methods = {
        "likes": like_based_recomended_podcasts,
        "subscriptions": subscription_based_recommended_podcasts,
    }

    def get(self, request, method):
        if method not in self.recommendations_methods:
            return Response({"details":"Recommendation method not found"}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        function = self.recommendations_methods[method]
        return Response(function(user))



class PodcastUpdateView(viewsets.ViewSet):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAdminUser,)


    @action(detail=False)
    def update_all(self, request, *args, **kwargs):
        # Explicit podcast update request
        update_podcasts_episodes.delay()
        return Response({}, status.HTTP_202_ACCEPTED)

    def update_single(self, request, *args, **kwargs):
        # Explicit podcast update request
        update_podcast.delay(podcast_id=kwargs["pk"])
        return Response({}, status.HTTP_202_ACCEPTED)
