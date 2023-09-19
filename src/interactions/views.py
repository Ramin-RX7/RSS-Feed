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



