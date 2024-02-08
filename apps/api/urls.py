from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views.courses import CourseViewSet
from apps.api.views.purchases import PurchaseViewSet, notification_link

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("purchases", PurchaseViewSet)

# TODO: https://djoser.readthedocs.io/en/latest/settings.html
urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("leadpay-notification/", notification_link, name="leadpay-notification"),
    path("", include(router.urls)),
]
