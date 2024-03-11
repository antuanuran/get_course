from rest_framework import serializers

from apps.api.serializers.base import BaseModelSerializer
from apps.holder.models import ImageHolder, LinkHolder, VideoHolder


class VideoHolderSerializer(BaseModelSerializer):
    class Meta:
        model = VideoHolder
        fields = ["uuid", "name", "description", "file"]

    name = serializers.CharField(max_length=100, required=False)


class ImageHolderSerializer(BaseModelSerializer):
    class Meta:
        model = ImageHolder
        fields = ["uuid", "name", "description", "file"]

    name = serializers.CharField(max_length=100, required=False)


class LinkHolderSerializer(BaseModelSerializer):
    class Meta:
        model = LinkHolder
        fields = ["uuid", "name", "description", "link"]
