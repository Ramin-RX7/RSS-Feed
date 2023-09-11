from rest_framework.serializers import ModelSerializer

from .models import PodcastRSS,PodcastEpisode,PodcastMainFields




class MainFieldsSerializer(ModelSerializer):
    class Meta:
        model = PodcastMainFields
        exclude = ("id",)

