from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.courses.models import Course, Lesson, Link, Video


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["description", "link"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["description", "video"]


class LessonSerializer(serializers.ModelSerializer):
    links = LinksSerializer(read_only=True, many=True)
    videos = VideoSerializer(read_only=True, many=True)
    lesson = serializers.CharField(source="name")

    class Meta:
        model = Lesson
        fields = ["lesson", "links", "videos"]


class CourseSerializer(TaggitSerializer, serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True)
    author_course = serializers.SlugRelatedField(slug_field="email", read_only=True, source="author")
    name_course = serializers.CharField(source="name")
    id_course = serializers.IntegerField(source="id")

    class Meta:
        model = Course
        fields = [
            "id_course",
            "name_course",
            "author_course",
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
