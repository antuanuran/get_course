from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.courses.models import Course


class CourseSerializer(TaggitSerializer, serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "id",
            "tags",
            "name",
            "description",
            "author",
            "product",
            "price",
            "poster",
            "is_sellable",
            "is_purchased",
            "is_favourite",
        ]

    tags = TagListSerializerField()
    is_purchased = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    def get_is_purchased(self, obj: Course) -> bool:
        user = self.context["request"].user
        return obj.purchases.filter(user=user).exists()

    def get_is_favourite(self, obj: Course) -> bool:
        user = self.context["request"].user
        return obj.favourites.filter(id=user.id).exists()
