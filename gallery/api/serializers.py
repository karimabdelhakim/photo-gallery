from django.contrib.auth import get_user_model
from rest_framework import serializers

from gallery.models import Gallery, Photo

User = get_user_model()


class GallerySerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Gallery
        fields = ["id", "user", "name", "likes_count", "public"]
        read_only_fields = ["user"]


class GalleryLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["number_of_likes"]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.likes.add(user)
        return instance


class PhotoSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Photo
        fields = ["id", "title", "description", "image", "gallery", "likes_count"]


class PhotoLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["number_of_likes"]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.likes.add(user)
        return instance
