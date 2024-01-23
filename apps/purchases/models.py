from django.db import models
from django.utils import timezone

from apps.courses.models import Course
from apps.users.models import User


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(default=timezone.now)
    price = models.PositiveIntegerField(blank=True)
    # available_courses (ManyToManyField: User)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.course.price
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Purchase №{self.id}"

    class Meta:
        verbose_name = "покупка"
        verbose_name_plural = "покупки"
