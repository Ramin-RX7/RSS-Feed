from rest_framework.serializers import ModelSerializer

from .models import PodcastRSS,PodcastEpisode,PodcastMainFields




class MainFieldsSerializer(ModelSerializer):
    class Meta:
        model = PodcastMainFields
        exclude = ("id",)



class PodcastRSSSerializer(ModelSerializer):
    # main_fields = MainFieldsSerializer()
    # field1 = serializers.CharField(source='main_fields.title')

    class Meta:
        model = PodcastRSS
        exclude = (
            "id",
            "name",
            "url",
            "created_at",
            "updated_at",
            "main_fields",
            "episode_attributes_path",
            "main_fields_path",
        )


    def to_representation(self, instance):
        main_fields_serializer = MainFieldsSerializer(instance.main_fields)
        rss_data = super().to_representation(instance)
        rss_data.update(main_fields_serializer.data)
        return rss_data
        # representation = super().to_representation(instance)
        # main_field_serializer = MainFieldsSerializer(instance.main_fields)
        # for field in main_field_serializer.get_fields():
            # representation[field] = main_field_serializer.data[field]
        # return representation




class PodcastEpisodeSerializer(ModelSerializer):
    class Meta:
        model = PodcastEpisode
        exclude = (
            "id",
            "rss",
            "created_at",
            "updated_at",
        )
