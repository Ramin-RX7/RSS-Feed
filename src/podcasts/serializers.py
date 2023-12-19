from rest_framework import serializers

from .models import PodcastRSS, PodcastEpisode, PodcastMainFields


class MainFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastMainFields
        exclude = ("id",)


class PodcastRSSSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastRSS
        fields = ["id"]

    def to_representation(self, instance):
        main_fields_serializer = MainFieldsSerializer(instance.main_fields)
        rss_data = super().to_representation(instance)
        rss_data.update(main_fields_serializer.data)
        return rss_data


class PodcastEpisodeSerializer(serializers.ModelSerializer):
    liked = serializers.BooleanField(read_only=True, required=False, default=False)

    class Meta:
        model = PodcastEpisode
        exclude = (
            # "id",
            "rss",
            "created_at",
            "updated_at",
        )
