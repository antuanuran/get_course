from django.core.exceptions import ValidationError
from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers

from apps.api.serializers.base import BaseModelSerializer
from apps.purchases.models import Purchase


class PurchaseSerializer(BaseModelSerializer):
    course = DynamicRelationField("apps.api.serializers.courses.CourseSerializer", read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Purchase
        fields = ["id", "course", "course_id", "purchased_at", "price", "status"]
        extra_kwargs = {
            "status": {"read_only": True},
            "purchased_at": {"read_only": True},
            "price": {"read_only": True},
        }

    def validate_course_id(self, value):
        if Purchase.objects.filter(course_id=value, user=self.context["request"].user).exists():
            raise ValidationError("already purchased")
        return value
