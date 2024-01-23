from django.urls import include, path

# TODO: https://djoser.readthedocs.io/en/latest/settings.html
urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
