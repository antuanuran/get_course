from django.db import models
from taggit.managers import TaggableManager

from apps.holder.models import ImageHolder, VideoHolder
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

    tags = TaggableManager(blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    poster = models.ImageField(upload_to="courses/posters/", null=True, blank=True)
    is_sellable = models.BooleanField(default=True)

    favourites = models.ManyToManyField(User, related_name="favourites", blank=True)
    # purchases (Course.purchases) - ForeighnKey - Purchase
    # lessons (Course.lessons) -  ForeighnKey - Lesson

    @property
    def free(self) -> bool:
        return self.price == 0

    def __str__(self) -> str:
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=100)
    annotation = models.TextField(null=True, blank=True)
    videos = models.ManyToManyField(VideoHolder, related_name="+", blank=True)
    # links (ForeignKey - Link)
    # tasks (ForeignKey - LessonTask)

    def __str__(self) -> str:
        return f"Занятие: {self.name} (курс: {self.course})"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "3. Уроки"

    @property
    def course_id(self):
        return self.lesson.course.id


class Link(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="links")
    link = models.URLField(max_length=500, unique=False, blank=True, null=True)
    description = models.TextField(null=True, blank=True)


class LessonTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    photo = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    auto_test = models.BooleanField(default=False)
    # possible_answers

    class Meta:
        verbose_name = "задание по уроку"
        verbose_name_plural = "_ Задания по уроку (Д/З)"

    def __str__(self) -> str:
        return f"Задание: {self.title} (курс: {self.lesson.course})"

    @property
    def course(self):
        return self.lesson.course.name


class LessonTaskAnswer(models.Model):
    task = models.ForeignKey(LessonTask, on_delete=models.CASCADE, related_name="possible_answers")
    text = models.TextField(null=True, blank=True)
    image = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    video = models.ForeignKey(VideoHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "ответ по Д/З"
        verbose_name_plural = "_ Ответы по Д/З"

    def __str__(self) -> str:
        return f"Ответ на задание: {self.task}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    task = models.ForeignKey(LessonTask, on_delete=models.CASCADE, related_name="user_answers")
    predefined_answers = models.ManyToManyField(LessonTaskAnswer, blank=True, related_name="+")
    custom_answer = models.TextField(null=True, blank=True)
    video = models.ForeignKey(VideoHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    photo = models.ForeignKey(ImageHolder, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    link = models.URLField(max_length=500, blank=True, null=True)
    success = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "результат ответа"
        verbose_name_plural = "_ Результаты ответов"

    def __str__(self) -> str:
        return self.task.title
