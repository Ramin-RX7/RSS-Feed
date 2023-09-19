from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from accounts.auth_backends import JWTAuthBackend
from podcasts.models import PodcastEpisode
from .serializers import *





class LikeView(generics.CreateAPIView):
    authentication_classes = (JWTAuthBackend,)
    permission_classes = (IsAuthenticated,)

    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        episode_id = request.data.get('episode_id')

        try:
            existing_like = Like.objects.get(user=user, episode=episode_id)
            existing_like.delete()
            return Response({'detail': 'Like removed successfully.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            like_data = {'user': user.id, 'episode': episode_id}
            serializer = self.get_serializer(data=like_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        episode_id = request.data.get('episode_id')
        user = request.user
        content = request.data.get('content')

        try:
            episode = PodcastEpisode.objects.get(pk=episode_id)
        except PodcastEpisode.DoesNotExist:
            return Response({"error": "Episode not found."}, status=status.HTTP_404_NOT_FOUND)

        comment_data = {'user': user.id, 'episode': episode.id, 'content': content}
        serializer = self.get_serializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


