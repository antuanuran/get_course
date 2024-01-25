from django.db import models

from apps.courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=100)
    annotation = models.TextField(null=True, blank=True)

    # videos
    # links


class Link(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="links")
    description = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=100, unique=False, blank=True)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="lessons/videos/", null=True, blank=True)
