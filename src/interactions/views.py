from django.utils.translation import gettext_lazy as _
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from accounts.auth_backends import JWTAuthBackend
from podcasts.models import PodcastEpisode
from .serializers import *





class LikeView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    serializer_class = LikeSerializer

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        episode_id = request.data.get('episode_id')
        # episode = PodcastEpisode.objects.get(id=episode_id)
        if not self.get_queryset().filter(episode=episode_id).exists():
            like = Like.objects.create(user=request.user, episode=episode_id)
            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"details":_("already liked")}, status=status.HTTP_208_ALREADY_REPORTED)

    @action(detail=True, methods=["POST"])
    def unlike(self, request, *args, **kwargs):
        episode_id = request.data.get('episode_id')
        like_qs = self.get_queryset().filter(episode=episode_id)
        if like_qs.exists():
            return Response({'detail': _('not liked yet')}, status=status.HTTP_406_NOT_ACCEPTABLE)
        like_qs.get().delete()
        return Response({'detail': _('Like removed successfully.')}, status=status.HTTP_202_ACCEPTED)


    def list(self, request, *args, **kwargs):
        """
        {
            "episodes": [EPISODE_ID, ]
        }
        """
        subscriptions = self.get_queryset().values_list("episode__id", flat=True)
        return Response({'episodes': list(subscriptions)}, status=status.HTTP_200_OK)




class CommentCreateView(generics.CreateAPIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        episode_id = request.data.get('episode_id')
        user = request.user
        content = request.data.get('content')

        try:
            episode = PodcastEpisode.objects.get(pk=episode_id)
        except PodcastEpisode.DoesNotExist:
            return Response({"error": _("Episode not found.")}, status=status.HTTP_404_NOT_FOUND)

        comment_data = {'user': user.id, 'episode': episode.id, 'content': content}
        serializer = self.get_serializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubscribeView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    serializer_class = SubscribeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        rss_id = request.data.get('rss_id')

        try:
            existing_like = Subscribe.objects.get(user=user, rss=rss_id)
            existing_like.delete()
            return Response({'detail': _('Subscribe removed successfully.')}, status=status.HTTP_200_OK)
        except Subscribe.DoesNotExist:
            like_data = {'user': user.id, 'rss': rss_id}
            serializer = self.get_serializer(data=like_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        {
            "podcasts": [PODCAST_ID, ]
        }
        """
        # subscriptions = Subscribe.objects.filter(user=request.user)
        # subscriptions = self.serializer_class(subscriptions, many=True)
        # return Response({'podcasts': list(subscriptions.data)}, status=status.HTTP_200_OK)
        subscriptions = Subscribe.objects.filter(user=request.user).values_list("rss__id", flat=True)
        return Response({'podcasts': list(subscriptions)}, status=status.HTTP_200_OK)
