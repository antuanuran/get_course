from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.api.serializers.courses import CourseSerializer
from apps.api.views.base import BaseModelViewSet
from apps.courses.models import Course


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Для вывода полного списка курсов - авторизация не обязательна", security=[]
    ),
)
class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, queryset=None):
        filter_params = Q(is_sellable=True)
        user = self.request.user
        if user.is_authenticated:
            filter_params |= Q(purchases__user=user) | Q(favourites=user)
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

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response("ok")

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response("ok")
