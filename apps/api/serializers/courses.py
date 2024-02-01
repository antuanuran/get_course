from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.api.serializers.base import BaseModelSerializer
from apps.api.serializers.users import UserSerializer
from apps.courses.models import Course, Lesson, Link


class LinkSerializer(BaseModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "description", "link"]


class LessonSerializer(BaseModelSerializer):
    links = DynamicRelationField(LinkSerializer, read_only=True, many=True)
    lesson = serializers.CharField(source="name")

    class Meta:
        model = Lesson
        fields = [
            "lesson",
            "id",
            "annotation",
            "links",
        ]


class CourseSerializer(TaggitSerializer, BaseModelSerializer):
    lessons = DynamicRelationField(LessonSerializer, read_only=True, many=True)
    author = DynamicRelationField(UserSerializer, read_only=True)
    name_course = serializers.CharField(source="name")
    id_course = serializers.IntegerField(source="id")

    class Meta:
        model = Course
        fields = [
            "id_course",
            "name_course",
            "author",
            "poster",
            "price",
            "tags",
            "description",
            "product",
            "is_sellable",
            "is_purchased",
            "is_favourite",
            "lessons",
        ]

    tags = TagListSerializerField()
    is_purchased = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    def get_is_purchased(self, obj: Course):
        current_user = self.context["request"].user.id
        return obj.purchases.filter(user_id=current_user).exists()

    def get_is_favourite(self, obj: Course):
        current_user = self.context["request"].user.id
        return obj.favourites.filter(id=current_user).exists()
