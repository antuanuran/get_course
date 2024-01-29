from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views.courses import CourseViewSet, import_file

router = DefaultRouter()
router.register("courses", CourseViewSet)

# TODO: https://djoser.readthedocs.io/en/latest/settings.html
urlpatterns = [
    path("", include("djoser.urls")),
    path("", include(router.urls)),
    path("import/", import_file),
    path("auth/", include("djoser.urls.jwt")),
]
