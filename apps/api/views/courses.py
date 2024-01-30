from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
        filter_params = Q(is_sellable=True)
        user = self.request.user
        if user.is_authenticated:
            filter_params |= Q(purchases__user=user) | Q(favourites=user)
        qs = super().get_queryset().filter(filter_params)
        # TODO: make annotations
        # qs = qs.annotate(is_purchased=Exists("purchased_courses"))
        return qs
