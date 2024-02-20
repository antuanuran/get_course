from dynamic_rest.fields import DynamicRelationField
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.api.serializers.base import BaseModelSerializer
from apps.api.serializers.holder import VideoSerializer
from apps.api.serializers.purchases import PurchaseSerializer
from apps.api.serializers.users import UserSerializer
from apps.courses.models import Course, Lesson, LessonTask, LessonTaskAnswer, Link


class LinkSerializer(BaseModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "description", "link"]


class LessonSerializer(BaseModelSerializer):
    links = DynamicRelationField(LinkSerializer, read_only=True, many=True)
    videos = DynamicRelationField(VideoSerializer, read_only=True, many=True)
    lesson = serializers.CharField(source="name")

    class Meta:
        model = Lesson
        fields = [
            "lesson",
            "id",
            "annotation",
            "links",
            "videos",
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
            "purchase",
            "is_favourite",
            "lessons",
        ]

    tags = TagListSerializerField()
    purchase = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

    def get_purchase(self, obj: Course):
        current_user = self.context["request"].user.id
        obj = obj.purchases.filter(user_id=current_user).first()
        if obj is None:
            return None
        return PurchaseSerializer(instance=obj).data

    def get_is_favourite(self, obj: Course):
        current_user = self.context["request"].user.id
        return obj.favourites.filter(id=current_user).exists()


class LessonTaskAnswerSerializer(BaseModelSerializer):
    task = DynamicRelationField("LessonTaskSerializer", read_only=True)

    class Meta:
        model = LessonTaskAnswer
        fields = ["id", "task", "text", "image"]


class LessonTaskSerializer(BaseModelSerializer):
    lessons = DynamicRelationField(LessonSerializer, read_only=True)
    possible_answers = DynamicRelationField(LessonTaskAnswerSerializer, read_only=True)

    class Meta:
        model = LessonTask
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "video",
            "auto_test",
            "possible_answers",
        ]
