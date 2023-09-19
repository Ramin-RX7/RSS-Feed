from rest_framework import serializers

from .models import Like,Comment,Subscribe




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ("id",)
