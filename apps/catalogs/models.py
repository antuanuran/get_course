# from django.db import models
# from django.core.validators import MinValueValidator
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     # products
#
#     class Meta:
#         verbose_name = "1. Направление"
#         verbose_name_plural = "1. Направления"
#
#     def __str__(self):
#         return self.name
#
#
# class Teacher(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     position = models.CharField(max_length=100, unique=True)
#     # products
#
#     class Meta:
#         verbose_name = "Преподаватель"
#         verbose_name_plural = "Преподаватели"
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
#     # teachers = models.ManyToManyField(Teacher, related_name="products", blank=True)
#     # versions
#     # courses
#
#     class Meta:
#         verbose_name = "2. Линейка курсов"
#         verbose_name_plural = "2. Линейки курсов"
#
#     def __str__(self):
#         return f"{self.name}"
#
#
# class Version(models.Model):
#     name = models.CharField(max_length=100)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="versions")
#     length = models.CharField(max_length=100)
#     certificate = models.CharField(max_length=100)
#
#     class Meta:
#         verbose_name = "Версия курса (стандарт / расширенная)"
#         verbose_name_plural = "Версии курса (стандарт / расширенная)"
#
#     def __str__(self):
#         return f"{self.name} [{self.product.name}]"
#
#
# class Course(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="courses")
#     level = models.CharField(max_length=100)  # Для новичков/Pro
#     upc = models.CharField(max_length=64, null=True, blank=True, db_index=True)
#
#     class Meta:
#         verbose_name = "3. Курс"
#         verbose_name_plural = "3. Курсы"
#
#     def __str__(self):
#         return f"{self.product.name} | Уровень: {self.level}"
#
#
# class Course_version(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_versions")
#     version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name="course_versions")
#     price = models.IntegerField(validators=[MinValueValidator(1)])
#
#     class Meta:
#         verbose_name = "Версия курса"
#         verbose_name_plural = "Версии курса"
#
#     def __str__(self):
#         return f"{self.price}"
