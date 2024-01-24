from django.db import models
from taggit.managers import TaggableManager

from apps.users.models import User


class Category(models.Model):
    class Meta:
        verbose_name = "направление/линейка курсов"
        verbose_name_plural = "направления/линейки курсов"

    name = models.CharField(max_length=100, unique=True)

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
        verbose_name_plural = "курсы"
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

    @property
    def free(self) -> bool:
        return self.price == 0

    def __str__(self) -> str:
        return self.name
