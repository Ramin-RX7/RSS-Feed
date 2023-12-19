from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from core.parser import *
from core.views import EpisodeListView
from accounts.auth_backends import JWTAuthBackend
from accounts.utils import auth_action
from interactions.models import Like, Subscribe, Comment
from .models import PodcastRSS, PodcastEpisode
from .serializers import PodcastRSSSerializer, PodcastEpisodeSerializer
from .utils import (
    like_based_recommended_podcasts,
    subscription_based_recommended_podcasts,
)
from .tasks import update_podcasts_episodes, update_podcast



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


class PodcastDetailView(generics.RetrieveAPIView, viewsets.ViewSet):
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

    @auth_action
    def subscribe(self, request, pk):
        rss = self.get_object()
        subscribe, created = Subscribe.objects.get_or_create(user=request.user, rss=rss)
        if created:
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": _("already subscribed")}, status=status.HTTP_208_ALREADY_REPORTED
        )

    @auth_action
    def unsubscribe(self, request, pk):
        subs_qs = Subscribe.objects.filter(user=request.user, rss=self.get_object())
        if not subs_qs.exists():
            return Response(
                {"detail": _("not subscribed yet")},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        subs_qs.get().delete()
        return Response(
            {"detail": _("Subscribe removed successfully.")},
            status=status.HTTP_202_ACCEPTED,
        )

    @auth_action
    def subscribers(self, request, pk):
        subscribers_list = Subscribe.objects.filter(rss=self.get_object()).values_list(
            "user__id", flat=True
        )
        return Response({"users": subscribers_list})

    @auth_action
    def notify_on(self, request, pk):
        rss = self.get_object()
        subscribe, created = Subscribe.objects.get_or_create(user=request.user, rss=rss)
        if subscribe.notification:
            return Response(
                {"detail": _("notification is already on for this podcast")},
                status=status.HTTP_208_ALREADY_REPORTED,
            )
        subscribe.notification = True
        subscribe.save()
        if created:
            return Response(
                {"detail": _("subscribed with notification on")},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": _("turned notification on")}, status.HTTP_202_ACCEPTED
        )

    @auth_action
    def notify_off(self, request, pk):
        rss = self.get_object()
        subscribe = Subscribe.objects.filter(user=request.user, rss=rss)
        if subscribe.exists():
            subscribe = subscribe.get()
            if subscribe.notification is False:
                return Response(
                    {"detail": _("notification is already off for this podcast")},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
            subscribe.notification = False
            subscribe.save()
            return Response(
                {"detail": _("turned notification off")}, status.HTTP_202_ACCEPTED
            )
        return Response(
            {"detail": _("not subscribed yet")}, status=status.HTTP_201_CREATED
        )


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

    @action(detail=True)
    def likes(self, request, *args, **kwargs):
        qs = Like.objects.filter(episode=self.get_object())
        users = qs.values_list("user", flat=True)
        return Response({"users": users, "count": len(users)})

    @auth_action
    def like(self, request, *args, **kwargs):
        episode = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, episode=episode)
        if created:
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": _("already liked")}, status=status.HTTP_208_ALREADY_REPORTED
        )

    @auth_action
    def unlike(self, request, *args, **kwargs):
        like_qs = Like.objects.filter(user=request.user, episode=self.get_object())
        if not like_qs.exists():
            return Response(
                {"detail": _("not liked yet")}, status=status.HTTP_406_NOT_ACCEPTABLE
            )
        like_qs.get().delete()
        return Response(
            {"detail": _("Like removed successfully.")}, status=status.HTTP_202_ACCEPTED
        )

    @auth_action
    def comment(self, request, *args, **kwargs):
        if content := request.data.get("content"):
            Comment.objects.create(
                user=request.user, content=content, episode=self.get_object()
            )
            return Response({}, status.HTTP_201_CREATED)
        return Response(
            {"detail": _("comment content not provided")},
            status.HTTP_406_NOT_ACCEPTABLE,
        )

    @action(detail=True)
    def comments(self, request, *args, **kwargs):
        return Response(
            list(
                Comment.objects.filter(episode=self.get_object()).values(
                    "user", "content", "created_at"
                )
            )
        )


class PodcastRecommendationView(APIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    recommendations_methods = {
        "likes": like_based_recommended_podcasts,
        "subscriptions": subscription_based_recommended_podcasts,
    }

    def get(self, request, method):
        if method not in self.recommendations_methods:
            return Response(
                {"details": _("Recommendation method not found")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = request.user
        function = self.recommendations_methods[method]
        return Response(function(user))


class PodcastUpdateView(viewsets.ViewSet):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAdminUser,)

    @action(detail=False)
    def update_all(self, request, *args, **kwargs):
        # Explicit podcast update request
        update_podcasts_episodes.delay(explicit_request=True)
        return Response({}, status.HTTP_202_ACCEPTED)

    def update_single(self, request, *args, **kwargs):
        # Explicit podcast update request
        update_podcast.delay(podcast_id=kwargs["pk"], explicit_request=True)
        return Response({}, status.HTTP_202_ACCEPTED)
