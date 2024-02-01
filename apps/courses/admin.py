from django.contrib import admin
from django.db.models import Count

from .models import Category, Course, Lesson, Link, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name_category", "count_products", "id"]
    inlines = [ProductInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(count_products=Count("products"))
        return qs

    @admin.display(description="кол-во линеек курсов", ordering="count_products")
    def count_products(self, obj):
        return obj.count_products

    @admin.display(description="направление", ordering="name_category")
    def name_category(self, obj):
        return obj.name


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name_course", "tag_list", "poster", "price", "author", "is_sellable", "free", "id"]
    list_filter = ["is_sellable"]
    filter_horizontal = ["favourites"]
    search_fields = ["name"]
    inlines = [LessonInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(tag_list=Count("tags"))
        return qs

    @admin.display(description="теги", ordering="tag_list")
    def tag_list(self, obj):
        return obj.tag_list

    @admin.display(boolean=True, ordering="price")
    def free(self, obj):
        return obj.free

    @admin.display(description="полное название курса", ordering="name")
    def name_course(self, obj):
        return obj.name


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


class VideoInline(admin.TabularInline):
    model = Lesson.videos.through
    extra = 0
    raw_id_fields = ["video"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["name_lesson", "course", "id"]
    inlines = [LinkInline, VideoInline]
    exclude = ["videos"]

    @admin.display(description="название урока", ordering="id")
    def name_lesson(self, obj):
        return f"Курс: {obj.course.name} (id курса={obj.course.id}). Название занятия: {obj.name}"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "category"]
