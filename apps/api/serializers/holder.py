from apps.api.serializers.base import BaseModelSerializer
from apps.holder.models import VideoHolder


class VideoSerializer(BaseModelSerializer):
    class Meta:
        model = VideoHolder
        fields = ["id", "name", "description", "file"]
