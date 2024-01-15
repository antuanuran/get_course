from django.contrib import admin

from .models import Category, Product, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "id"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "poster", "author", "price", "free"]
