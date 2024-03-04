from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.api.permissions import IsAuthorOrReadOnly, is_author_builder
from apps.api.serializers.courses import (
    CommentSerializer,
    CourseSerializer,
    LessonSerializer,
    LessonTaskSerializer,
    ReviewSerializer,
    UserAnswerSerializer,
)
from apps.api.views.base import BaseModelViewSet
from apps.courses.models import Comment, Course, Lesson, LessonTask, Review, UserAnswer
from apps.purchases.models import Purchase


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Для вывода полного списка курсов - авторизация не обязательна",
        security=[],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Для вывода конкретного курса - авторизация не обязательна",
        security=[],
    ),
)
class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self, queryset=None):
        filter_params = Q(is_sellable=True)
        user = self.request.user
        if user.is_authenticated:
            filter_params |= Q(purchases__user=user) | Q(favourites=user) | Q(author=user)
        qs = super().get_queryset(queryset).filter(filter_params)
        # TODO: make annotations
        # qs = qs.annotate(is_purchased=Exists("purchased_courses"))
        return qs

    @swagger_auto_schema(request_body=no_body)
    @action(detail=True, methods=["post"], url_path="toggle-favourite", permission_classes=[IsAuthenticated])
    def toggle_favourite(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if course.favourites.filter(id=user.id).exists():
            course.favourites.remove(user)
        else:
            course.favourites.add(user)
        serializer = self.get_serializer(instance=course)
        return Response(serializer.data)


class ReviewViewSet(BaseModelViewSet):
    queryset = Review.objects.filter(is_published=True)
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "post", "delete", "options", "head"]

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data.get("course")
        if not Purchase.objects.filter(course=course, user=user, status=Purchase.Status.COMPLETED).exists():
            raise PermissionDenied("course was not purchased")
        serializer.save(author=self.request.user)


class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    http_method_names = ["get", "post", "delete", "options", "head"]

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data["lesson"].course
        if not Purchase.objects.filter(course=course, user=user, status=Purchase.Status.COMPLETED).exists():
            raise PermissionDenied("course was not purchased")
        serializer.save(author=user)


class LessonViewSet(BaseModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        user = self.request.user
        filter_params = Q(
            course__purchases__user=user,
            course__purchases__status=Purchase.Status.COMPLETED,
        ) | Q(course__author=user)
        qs = super().get_queryset(queryset).filter(filter_params)
        return qs


class LessonTaskViewSet(BaseModelViewSet):
    queryset = LessonTask.objects.all()
    serializer_class = LessonTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, queryset=None):
        user = self.request.user
        filter_params = Q(
            lesson__course__purchases__user=user,
            lesson__course__purchases__status=Purchase.Status.COMPLETED,
        ) | Q(lesson__course__author=user)
        qs = super().get_queryset(queryset).filter(filter_params)
        return qs


class UserAnswerViewSet(BaseModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated, is_author_builder("user")]
    http_method_names = ["get", "post"]

    def get_queryset(self, queryset=None):
        user = self.request.user
        filter_params = Q(user=user) | Q(task__lesson__course__author=user)
        qs = super().get_queryset(queryset).filter(filter_params)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data.get("task").lesson.course
        if not Purchase.objects.filter(course=course, user=user, status=Purchase.Status.COMPLETED).exists():
            raise PermissionDenied("course was not purchased")
        serializer.save(user=self.request.user)

        user_answer = serializer.instance
        task = user_answer.task
        if task.auto_test:
            correct_answers = set(task.possible_answers.filter(is_correct=True).values_list("id", flat=True))
            user_answers = set(user_answer.predefined_answers.values_list("id", flat=True))
            user_answer.success = correct_answers == user_answers
            user_answer.finished_at = timezone.now()
            user_answer.save(update_fields=["success", "finished_at"])
