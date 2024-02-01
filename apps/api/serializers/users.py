from apps.api.serializers.base import BaseModelSerializer
from apps.users.models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
