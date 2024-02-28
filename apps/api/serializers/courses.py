from django.core.exceptions import ValidationError
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField
from taggit.serializers import TaggitSerializer, TagListSerializerField

from apps.api.serializers.base import BaseModelSerializer
from apps.api.serializers.holder import ImageHolderSerializer, LinkHolderSerializer, VideoHolderSerializer
from apps.api.serializers.purchases import PurchaseSerializer
from apps.api.serializers.users import UserSerializer
from apps.courses.models import Category, Course, Lesson, LessonTask, LessonTaskAnswer, Product, UserAnswer


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
        ]

    def get_is_purchased(self, obj: Course):
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
