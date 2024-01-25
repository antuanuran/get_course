from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from apps.api.serializers.courses import CourseSerializer
from apps.courses.models import Course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # user = self.request.user
        qs = super().get_queryset()
        # TODO: make annotations
        # qs = qs.annotate(is_purchased=Exists("purchased_courses"))
        return qs
