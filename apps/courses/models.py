from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from ordered_model.models import OrderedModel
from taggit.managers import TaggableManager

from apps.holder.models import ImageHolder, LinkHolder, VideoHolder
from apps.users.models import User


class Category(models.Model):
    class Meta:
        verbose_name = "направление/линейка курсов"
        verbose_name_plural = "1. Направления/линейки курсов"

    name = models.CharField(max_length=100, unique=True)
    # products

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "линейка курсов"
        verbose_name_plural = "линейки курсов"
        constraints = [
            models.UniqueConstraint(fields=["category", "name"], name="unique_product_name_per_category"),
        ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "2. Курсы"
        constraints = [
            models.UniqueConstraint(fields=["product", "name"], name="unique_course_name_per_product"),
        ]

    class OpenType(models.TextChoices):
        instant = "instant", "Открывается сразу все при покупке"
        schedule = "schedule", "Открывается по расписанию в уроках"
        progress = "progress", "Открывается по успешному прохождению предыдущего урока"

    tags = TaggableManager(blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    poster = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    is_sellable = models.BooleanField(default=True)
    open_type = models.CharField(max_length=16, choices=OpenType.choices, default=OpenType.instant)

    curators = models.ManyToManyField(User, related_name="managed_courses", blank=True)
    favourites = models.ManyToManyField(User, related_name="favourites", blank=True)
    # purchases (Course.purchases) - ForeighnKey - Purchase
    # lessons (Course.lessons) -  ForeighnKey - Lesson

    @property
    def free(self) -> bool:
        return self.price == 0

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "4. Отзывы к курсу"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    images = models.ManyToManyField(ImageHolder, related_name="+", blank=True)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(10)])
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)


class Lesson(OrderedModel):
    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "3. Уроки"
        ordering = ("course", "order")

    # order = ...
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=100)
    annotation = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    open_time = models.DateTimeField(null=True, blank=True)
    videos = models.ManyToManyField(VideoHolder, related_name="+", blank=True)
    images = models.ManyToManyField(ImageHolder, related_name="+", blank=True)
    links = models.ManyToManyField(LinkHolder, related_name="+", blank=True)
    # tasks (ForeignKey - LessonTask)
    # comments

    order_with_respect_to = "course"

    def __str__(self) -> str:
        return f"Занятие: {self.name} (курс: {self.course})"


class Comment(models.Model):
    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "5. Комментарии к урокам"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    images = models.ManyToManyField(ImageHolder, related_name="+", blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class LessonTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(ImageHolder, related_name="+", blank=True)
    videos = models.ManyToManyField(VideoHolder, related_name="+", blank=True)
    links = models.ManyToManyField(LinkHolder, related_name="+", blank=True)
    auto_test = models.BooleanField(default=False)
    # possible_answers

    class Meta:
        verbose_name = "задание по уроку"
        verbose_name_plural = "3.1 Задания по уроку (Task)"

    def __str__(self) -> str:
        return f"{self.title} | task: id={self.id}"

    @property
    def course(self) -> Course:
        return self.lesson.course


class LessonTaskAnswer(models.Model):
    task = models.ForeignKey(LessonTask, on_delete=models.CASCADE, related_name="possible_answers")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "вариант ответов"
        verbose_name_plural = "Варианты ответов (predefined_answers)"

    def __str__(self) -> str:
        return f"predefined_answer: id = {self.id}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    task = models.ForeignKey(LessonTask, on_delete=models.CASCADE, related_name="user_answers")
    predefined_answers = models.ManyToManyField(LessonTaskAnswer, blank=True, related_name="+")
    custom_answer = models.TextField(null=True, blank=True)
    video = models.ForeignKey(VideoHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    image = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    link = models.ForeignKey(LinkHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    success = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_checked(self) -> bool:
        return self.finished_at is not None

    class Meta:
        verbose_name = "результат ответа"
        verbose_name_plural = "3.2 Результаты ответов (UserAnswer)"

    def __str__(self) -> str:
        return f" task: {self.task.title}"


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    pdf = models.FileField(upload_to="files/certificates/", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name = "сертификат"
    #     verbose_name_plural = "6. Сертификат"
