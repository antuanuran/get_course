from apps.api.serializers.base import BaseModelSerializer
from apps.holder.models import Video


class VideoSerializer(BaseModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "name", "description", "file"]
