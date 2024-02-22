from django.contrib import admin

from apps.holder.models import ImageHolder, VideoHolder


@admin.register(VideoHolder)
class VideoHolderAdmin(admin.ModelAdmin):
    list_display = ["name", "file", "id"]


@admin.register(ImageHolder)
class ImageHolderAdmin(admin.ModelAdmin):
    list_display = ["name", "file", "id"]
