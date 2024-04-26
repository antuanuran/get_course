from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views.courses import (
    CommentViewSet,
    CourseViewSet,
    LessonTaskViewSet,
    LessonViewSet,
    ReviewViewSet,
    UserAnswerViewSet,
)
from apps.api.views.holder import upload_image_view, upload_link_view, upload_video_view
from apps.api.views.purchases import PurchaseViewSet, fake_leadpay_link, notification_link
from apps.api.views.tg_webhook import tg_callback

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("reviews", ReviewViewSet)
router.register("comments", CommentViewSet)
router.register("lessons", LessonViewSet)
router.register("lesson-tasks", LessonTaskViewSet)
router.register("purchases", PurchaseViewSet)
router.register("user-answers", UserAnswerViewSet)


# TODO: https://djoser.readthedocs.io/en/latest/settings.html
urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("", include("djoser.urls")),
    path("leadpay-notification/", notification_link, name="leadpay-notification"),
    path("fake-leadpay-link/", fake_leadpay_link),
    path("", include(router.urls)),
    path("media/images/", upload_image_view),
    path("media/videos/", upload_video_view),
    path("media/links/", upload_link_view),
    path("tg-callback/<str:token>/", tg_callback),
]
