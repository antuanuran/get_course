from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.api.serializers.courses import CourseSerializer
from apps.courses.models import Course


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]

    filterset_fields = ["product"]
    # search_fields = []

    def get_queryset(self):
        # user = self.request.user
        qs = super().get_queryset()
        # TODO: make annotations
        # qs = qs.annotate(is_purchased=Exists("purchased_courses"))
        return qs


@api_view(http_method_names=["post"])
def import_file(request):
    if not request.FILES or "file" not in request.FILES:
        raise ValidationError("no file", code="no-file")

    else:
        data_stream = request.FILES["file"]
        print(data_stream)

    return Response(
        data=f"file: '{request.FILES['file'].name}' LOAD......ok",
        status=status.HTTP_201_CREATED,
    )
