from django.contrib import admin

from apps.holder.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["name", "file", "id"]
