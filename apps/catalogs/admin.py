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

    # 1 часть кода - выпадающий список
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "version":
            if getattr(request, "_product_instance", None) is not None:
                field.queryset = field.queryset.filter(product=request._product_instance)
            else:
                field.queryset = field.queryset.none()
        return field

    # ********************************


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["product", "level", "id"]
    inlines = [Course_versionInlines]

    # 2 часть кода - выпадающий список*******************************#
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["product"]
        else:
            return super().get_readonly_fields(request, obj=None)

    def get_form(self, request, obj=None, **kwargs):
        request._product_instance = getattr(obj, "product", None)
        return super().get_form(request, obj, **kwargs)

    # ****************************************************************#

    # Защита от редактирования Продукта
    def get_inlines(self, request, obj):
        if obj:
            return super().get_inlines(request, obj)
        else:
            return []


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["name", "position"]
