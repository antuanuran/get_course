from apps.api.serializers.base import BaseModelSerializer
from apps.holder.models import ImageHolder, LinkHolder, VideoHolder


class VideoHolderSerializer(BaseModelSerializer):
    class Meta:
        model = VideoHolder
        fields = ["id", "name", "description", "file"]


class ImageHolderSerializer(BaseModelSerializer):
    class Meta:
        model = ImageHolder
        fields = ["id", "name", "description", "file"]


class LinkHolderSerializer(BaseModelSerializer):
    class Meta:
        model = LinkHolder
        fields = ["id", "name", "description", "link"]
