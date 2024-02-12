from django.db import models
from django.utils import timezone

from apps.courses.models import Course
from apps.users.models import User


class Purchase(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED"
        CANCELED_BY_USER = "CANCELED_BY_USER"
        CANCELED_BY_MANAGER = "CANCELED_BY_MANAGER"
        REFUND = "REFUND"
        COMPLETED = "COMPLETED"
        SUSPECTED = "SUSPECTED"
        FAILED = "FAILED"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(default=timezone.now)
    price = models.PositiveIntegerField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
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
        constraints = [
            models.UniqueConstraint(name="unique_course_per_user", fields=["user", "course"]),
        ]


class LinkPay(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="links_pays")
    reference = models.URLField(max_length=500, unique=False, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.reference is None:
    #         self.reference = f"http://link/"
    #     return super().save(*args, **kwargs)
