from django.contrib import admin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from .models import Category, Course, Lesson, LessonTask, LessonTaskAnswer, Product, UserAnswer


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
    exclude = ["videos"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name_course", "sellable", "tag_list", "poster", "price", "author", "is_sellable", "free", "id"]
    list_filter = ["is_sellable"]
    list_editable = ["is_sellable"]
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

    @admin.display(description="активировать / закрыть курс")
    def sellable(self, obj: Course):
        link = reverse("admin:sel", args=[obj.id])
        return mark_safe(f"<a href='{link}'>вкл/выкл</a>")

    def get_urls(self):
        urls = [
            path("<obj_id>/sellable/", self.sellable_viewset, name="sel"),
        ] + super().get_urls()
        return urls

    def sellable_viewset(self, request, obj_id, *args, **kwargs):
        obj = get_object_or_404(Course, id=obj_id)
        obj.is_sellable = not obj.is_sellable
        obj.save(update_fields=["is_sellable"])
        return redirect(reverse("admin:courses_course_changelist"))


class VideoInline(admin.TabularInline):
    model = Lesson.videos.through
    extra = 0
    # raw_id_fields = ["video"]


class LessonTaskInline(admin.TabularInline):
    model = LessonTask
    extra = 0
    exclude = ["description", "photo", "auto_test"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["name_lesson", "course", "course_id", "id"]
    inlines = [VideoInline, LessonTaskInline]
    exclude = ["videos"]

    @admin.display(description="название урока", ordering="id")
    def name_lesson(self, obj):
        return obj.name


class LessonTaskAnswerInline(admin.TabularInline):
    model = LessonTaskAnswer
    extra = 0


@admin.register(LessonTask)
class LessonTaskAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "course", "auto_test", "id"]
    list_editable = ["auto_test"]
    inlines = [LessonTaskAnswerInline]


@admin.register(LessonTaskAnswer)
class LessonTaskAnswerAdmin(admin.ModelAdmin):
    list_display = ["task", "is_correct", "id"]


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ["task", "user", "success", "id"]
