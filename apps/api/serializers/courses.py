import re

from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils import timezone
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.api.serializers.base import BaseModelSerializer
from apps.api.serializers.holder import ImageHolderSerializer, LinkHolderSerializer, VideoHolderSerializer
from apps.api.serializers.purchases import PurchaseSerializer
from apps.api.serializers.users import UserSerializer
from apps.courses.models import (
    Category,
    Comment,
    Course,
    Lesson,
    LessonTask,
    LessonTaskAnswer,
    Product,
    Review,
    UserAnswer,
)
from apps.utilities.models import BlacklistedWord


class CategorySerializer(BaseModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]


class ProductSerializer(BaseModelSerializer):
    category = DynamicRelationField(CategorySerializer, read_only=True)

    class Meta:
        model = Product
        fields = ["name", "id", "category"]


class LessonSerializer(BaseModelSerializer):
    videos = DynamicRelationField(VideoHolderSerializer, read_only=True, many=True)
    images = DynamicRelationField(ImageHolderSerializer, read_only=True, many=True)
    links = DynamicRelationField(LinkHolderSerializer, read_only=True, many=True)
    tasks = DynamicRelationField("LessonTaskSerializer", read_only=True, many=True)
    course = DynamicRelationField("CourseSerializer", read_only=True)
    comments = DynamicRelationField("CommentSerializer", many=True)
    is_available = DynamicMethodField(requires=["course"])

    def get_is_available(self, obj: Lesson):
        if obj.course.open_type == obj.course.OpenType.instant:
            return True
        if obj.course.open_type == obj.course.OpenType.schedule:
            return obj.open_time <= timezone.now()
        if obj.course.open_type == obj.course.OpenType.progress:
            for lesson in obj.course.lessons.annotate(task_count=Count("tasks")).all():
                if lesson.order >= obj.order:
                    return True
                if lesson.task_count == 0:
                    continue
                if not lesson.tasks.filter(user_answers__success=True).exists():
                    break
            return False
        return False

    class Meta:
        model = Lesson
        fields = [
            "name",
            "id",
            "annotation",
            "text",
            "videos",
            "images",
            "links",
            "tasks",
            "course",
            "comments",
            "is_available",
        ]


class CourseSerializer(TaggitSerializer, BaseModelSerializer):
    lessons = DynamicRelationField(LessonSerializer, read_only=True, many=True)
    author = DynamicRelationField(UserSerializer, read_only=True)
    product = DynamicRelationField(ProductSerializer, read_only=True)
    poster = DynamicRelationField(ImageHolderSerializer, read_only=True)
    tags = TagListSerializerField()
    is_purchased = DynamicMethodField()
    is_favourite = DynamicMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "author",
            "product",
            "poster",
            "price",
            "tags",
            "description",
            "product",
            "is_sellable",
            "is_purchased",
            "is_favourite",
            "lessons",
            "open_type",
        ]
        read_only_fields = ["open_type"]

    def get_is_purchased(self, obj: Course):
        current_user = self.context["request"].user.id
        obj = obj.purchases.filter(user_id=current_user).first()
        if obj is None:
            return None
        return PurchaseSerializer(instance=obj).data

    def get_is_favourite(self, obj: Course):
        current_user = self.context["request"].user.id
        return obj.favourites.filter(id=current_user).exists()


class ReviewSerializer(BaseModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "author", "course", "text", "rating", "images"]

    author = DynamicRelationField(UserSerializer, read_only=True)
    course = DynamicRelationField(CourseSerializer)
    images = DynamicRelationField(ImageHolderSerializer, many=True)

    def validate_text(self, value: str) -> str:
        blacklisted_words = BlacklistedWord.objects.values_list("word", flat=True)
        if not blacklisted_words:
            return value
        # TODO: escape symbols
        blacklisted_words = "|".join(blacklisted_words)
        pattern = re.compile(blacklisted_words, re.IGNORECASE)
        return pattern.sub("***", value)


class CommentSerializer(BaseModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "lesson", "text", "images", "created_at"]

    author = DynamicRelationField(UserSerializer, read_only=True)
    lesson = DynamicRelationField(LessonSerializer)
    images = DynamicRelationField(ImageHolderSerializer, many=True)

    def validate_text(self, value: str) -> str:
        blacklisted_words = BlacklistedWord.objects.values_list("word", flat=True)
        if not blacklisted_words:
            return value
        blacklisted_words = "|".join(blacklisted_words)
        pattern = re.compile(blacklisted_words, re.IGNORECASE)
        return pattern.sub("***", value)


class LessonTaskAnswerSerializer(BaseModelSerializer):
    task = DynamicRelationField("LessonTaskSerializer", read_only=True)

    class Meta:
        model = LessonTaskAnswer
        fields = ["id", "task", "text"]


class LessonTaskSerializer(BaseModelSerializer):
    lesson = DynamicRelationField(LessonSerializer, read_only=True)
    possible_answers = DynamicRelationField(LessonTaskAnswerSerializer, read_only=True, many=True)
    videos = DynamicRelationField(VideoHolderSerializer, read_only=True, many=True)
    images = DynamicRelationField(ImageHolderSerializer, read_only=True, many=True)
    links = DynamicRelationField(LinkHolderSerializer, read_only=True, many=True)

    class Meta:
        model = LessonTask
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "images",
            "videos",
            "links",
            "auto_test",
            "possible_answers",
        ]


class UserAnswerSerializer(BaseModelSerializer):
    user = DynamicRelationField(UserSerializer, read_only=True)
    task = DynamicRelationField(LessonTaskSerializer)
    predefined_answers = DynamicRelationField(LessonTaskAnswerSerializer, many=True)
    video = DynamicRelationField(VideoHolderSerializer)
    image = DynamicRelationField(ImageHolderSerializer)
    link = DynamicRelationField(LinkHolderSerializer)

    class Meta:
        model = UserAnswer
        fields = [
            "id",
            "user",
            "task",
            "predefined_answers",
            "custom_answer",
            "video",
            "image",
            "link",
            "success",
            "finished_at",
        ]

    def validate_task(self, task: LessonTask) -> LessonTask:
        user = self.context["request"].user
        if UserAnswer.objects.filter(user=user, task=task).exists():
            raise ValidationError("answer already exists")
        return task

    def validate(self, attrs: dict) -> dict:
        predefined_answers = attrs.get("predefined_answers", [])
        task = attrs["task"]
        if predefined_answers:
            possible_answers = set(task.possible_answers.values_list("id", flat=True))
            predefined_answers = {x.id for x in predefined_answers}
            if not predefined_answers.issubset(possible_answers):
                raise ValidationError({"predefined_answers": "detected strange answers"})
        return attrs
