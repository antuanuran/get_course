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
        super().save(*args, **kwargs)

        from apps.bot.service import pay_purchases

        if self.status == self.Status.COMPLETED:
            pay_purchases(self.user.email, self.course.name)

    def __str__(self) -> str:
        return f"Purchase №{self.id}"

    class Meta:
        verbose_name = "покупка"
        verbose_name_plural = "покупки"
        constraints = [
            models.UniqueConstraint(name="unique_course_per_user", fields=["user", "course"]),
        ]
