from django.db import models

from apps.courses.models import Lesson


class Video(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    video_link = models.FileField(upload_to="files/videos/", max_length=500, null=True, blank=True)
    lessons = models.ManyToManyField(Lesson, related_name="videos", blank=True)

    class Meta:
        verbose_name = "видео-файл"
        verbose_name_plural = "видео-файлы"

    def __str__(self) -> str:
        return self.name
