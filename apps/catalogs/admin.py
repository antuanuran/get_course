from django.contrib import admin

from .models import Category, Product, Teacher, Version, Course, Course_version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class VersionInlines(admin.TabularInline):
    model = Version
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    inlines = [VersionInlines]


class Course_versionInlines(admin.TabularInline):
    model = Course_version
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["product", "level", "id"]
    inlines = [Course_versionInlines]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["name", "position"]
